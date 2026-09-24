"""
Regression tests for sheets_helper.py's _write_row() - specifically the shape of the Sheets API
batch_update request it sends.

Real production bug: rows used to be inserted at the top of the sheet (insertDimension, right
after the header) rather than appended at the bottom. Sheets has to shift every existing row down
by one on every single write done that way - cheap on a small sheet, but the two tabs this feature
actually writes to had each grown to 40,000+ rows over time, and that shift became the dominant
cost of a write: confirmed via direct measurement that the very first write of a run (which also
has to fetch the whole workbook's metadata - itself slower on such a large sheet - before the
first write can happen) took 38+ seconds, consistently, every run, not as a one-off network
hiccup. Switched to appendCells, which the Sheets API appends after the sheet's own last row with
data automatically - no row-shifting, no need to track a row index ourselves. The existing ~40k
rows in both real tabs were separately reversed (oldest-first) and their inflated trailing blank
rows trimmed, as a one-time manual migration to match this new append direction - not something
this test suite covers.
"""
import pytest

import sheets_helper


class FakeSpreadsheet:
    def __init__(self):
        self.batch_update_calls = []

    def batch_update(self, body):
        self.batch_update_calls.append(body)
        return {}


class FakeWorksheet:
    def __init__(self):
        self.id = 12345
        self.spreadsheet = FakeSpreadsheet()


def test_write_row_appends_instead_of_inserting_at_the_top(monkeypatch):
    """The whole point of the fix: no insertDimension request (which shifts every existing row
    down) - an appendCells request instead (which Sheets appends after its own last row with data,
    with no shifting cost)."""
    ws = FakeWorksheet()
    monkeypatch.setattr(sheets_helper, "_get_worksheet", lambda *args, **kwargs: ws)

    ok, error = sheets_helper._write_row("sheet-id", "tab", ["2026-01-01", "some text"], "client.json", "token.json")

    assert ok is True
    assert error is None
    assert len(ws.spreadsheet.batch_update_calls) == 1
    requests = ws.spreadsheet.batch_update_calls[0]["requests"]
    request_types = [next(iter(request)) for request in requests]
    assert request_types == ["appendCells"], f"expected only an appendCells request, got {request_types}"


def test_write_row_appends_cells_with_correct_values_and_formats(monkeypatch):
    """The appended row must still carry the same date-serial value + DATE format for column A, and
    TEXT format for column B, that the old insertDimension+updateCells pair used to set - switching
    how the row lands must not change what's actually written."""
    ws = FakeWorksheet()
    monkeypatch.setattr(sheets_helper, "_get_worksheet", lambda *args, **kwargs: ws)

    sheets_helper._write_row("sheet-id", "tab", ["2026-01-15", "Track - Artist (Album)"], "client.json", "token.json")

    append_request = ws.spreadsheet.batch_update_calls[0]["requests"][0]["appendCells"]
    assert append_request["sheetId"] == ws.id
    assert append_request["fields"] == "userEnteredValue,userEnteredFormat.numberFormat"
    values = append_request["rows"][0]["values"]
    assert values[0]["userEnteredValue"]["numberValue"] == sheets_helper._date_to_serial("2026-01-15")
    assert values[0]["userEnteredFormat"]["numberFormat"]["type"] == "DATE"
    assert values[1]["userEnteredValue"]["stringValue"] == "Track - Artist (Album)"
    assert values[1]["userEnteredFormat"]["numberFormat"]["type"] == "TEXT"


def test_write_row_still_retries_transient_errors_after_switching_to_append(monkeypatch):
    """The retry-with-backoff behavior for transient (429/5xx) errors must survive the
    insertDimension -> appendCells switch unchanged."""
    ws = FakeWorksheet()
    attempts = []

    class FlakyResponse:
        status_code = 429

    class FlakyError(Exception):
        def __init__(self):
            self.response = FlakyResponse()

    def flaky_batch_update(body):
        attempts.append(body)
        if len(attempts) < 2:
            raise FlakyError()
        return {}

    ws.spreadsheet.batch_update = flaky_batch_update
    monkeypatch.setattr(sheets_helper, "_get_worksheet", lambda *args, **kwargs: ws)
    monkeypatch.setattr(sheets_helper.time, "sleep", lambda seconds: None)

    ok, error = sheets_helper._write_row("sheet-id", "tab", ["2026-01-01", "some text"], "client.json", "token.json")

    assert ok is True
    assert error is None
    assert len(attempts) == 2
    assert next(iter(attempts[0]["requests"][0])) == "appendCells"


# Regression: gspread's own Client.open_by_key() (via Spreadsheet.__init__()) and
# Spreadsheet.worksheet() each independently call fetch_sheet_metadata() to get the same workbook
# metadata - confirmed by direct measurement that this single call alone can cost anywhere from a
# couple of seconds to 20+ seconds against a large, long-lived spreadsheet, so doing it twice for
# one worksheet lookup was routinely the single most expensive part of a cold write, separately
# from (and in addition to) the insertDimension-vs-appendCells row-shifting cost above.
class _FakeGspreadWorksheet:
    def __init__(self, spreadsheet, properties, spreadsheet_id, client):
        self.spreadsheet = spreadsheet
        self.properties = properties
        self.spreadsheet_id = spreadsheet_id
        self.client = client


class _FakeGspreadSpreadsheet:
    pass


class _FakeGspreadModule:
    Spreadsheet = _FakeGspreadSpreadsheet
    Worksheet = _FakeGspreadWorksheet


def test_open_worksheet_single_fetch_makes_exactly_one_metadata_call(monkeypatch):
    fetch_calls = []

    class FakeHTTPClient:
        def fetch_sheet_metadata(self, spreadsheet_id):
            fetch_calls.append(spreadsheet_id)
            return {
                "properties": {"title": "My Spreadsheet"},
                "sheets": [
                    {"properties": {"title": "Other", "sheetId": 1}},
                    {"properties": {"title": "JMK", "sheetId": 2}},
                ],
            }

    class FakeClient:
        def __init__(self):
            self.http_client = FakeHTTPClient()

        def open_by_key(self, spreadsheet_id):
            raise AssertionError("the slow fallback path must not run when the fast path succeeds")

    monkeypatch.setattr(sheets_helper, "gspread", _FakeGspreadModule)

    sh, ws = sheets_helper._open_worksheet_single_fetch(FakeClient(), "sheet-id", "JMK")

    assert fetch_calls == ["sheet-id"], "must call fetch_sheet_metadata exactly once, not via open_by_key() + worksheet()"
    assert ws.properties["title"] == "JMK"
    assert sh._properties["id"] == "sheet-id"
    assert sh._properties["title"] == "My Spreadsheet"


def test_open_worksheet_single_fetch_falls_back_when_the_fast_path_breaks(monkeypatch):
    """If the fast path ever breaks (e.g. a future gspread version renames the internal attributes
    it relies on), fall back to the normal, slower, double-fetch gspread path rather than crashing
    outright - correctness over speed if the two ever diverge."""
    class FakeHTTPClient:
        def fetch_sheet_metadata(self, spreadsheet_id):
            raise RuntimeError("simulated internal gspread change breaking the fast path")

    class FakeFallbackWorksheet:
        title = "JMK"

    class FakeFallbackSpreadsheet:
        def worksheet(self, tab_name):
            return FakeFallbackWorksheet()

    class FakeClient:
        def __init__(self):
            self.http_client = FakeHTTPClient()

        def open_by_key(self, spreadsheet_id):
            return FakeFallbackSpreadsheet()

    monkeypatch.setattr(sheets_helper, "gspread", _FakeGspreadModule)

    sh, ws = sheets_helper._open_worksheet_single_fetch(FakeClient(), "sheet-id", "JMK")

    assert ws.title == "JMK"


def test_open_worksheet_single_fetch_falls_back_when_the_tab_is_not_found(monkeypatch):
    """A tab name absent from the fetched metadata must still surface gspread's own
    WorksheetNotFound (via the fallback path), not a raw, confusing StopIteration."""
    class FakeHTTPClient:
        def fetch_sheet_metadata(self, spreadsheet_id):
            return {"properties": {"title": "My Spreadsheet"}, "sheets": [{"properties": {"title": "Other"}}]}

    class FakeClient:
        def __init__(self):
            self.http_client = FakeHTTPClient()
            self.fell_back = False

        def open_by_key(self, spreadsheet_id):
            self.fell_back = True

            class FallbackSpreadsheet:
                def worksheet(self, tab_name):
                    raise KeyError("simulated gspread.exceptions.WorksheetNotFound")

            return FallbackSpreadsheet()

    monkeypatch.setattr(sheets_helper, "gspread", _FakeGspreadModule)
    client = FakeClient()

    with pytest.raises(KeyError):
        sheets_helper._open_worksheet_single_fetch(client, "sheet-id", "MissingTab")
    assert client.fell_back is True
