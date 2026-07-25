# sheets_helper.py
#
# Direct Google Sheets integration for spotify_monitor.py, replacing the Gmail-scraping
# Google Apps Script (jmk_script.txt / kel_script.txt) with a live write from the monitor
# itself. Authenticates via a one-time OAuth desktop consent flow, caching a refresh token
# so subsequent runs are unattended.
#
# Every write goes through update_spreadsheet(), which also owns a local file-based queue:
# if a write fails, the row is queued instead of lost, and is retried (in order) on the
# next call before any new row is attempted. Callers get told whether this call is the
# moment the failure started or the moment the queue fully drained, so they can alert once
# per transition instead of on every retry.

import os
import json

try:
    import gspread
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    LIBS_AVAILABLE = True
    IMPORT_ERROR = None
except ImportError as e:
    LIBS_AVAILABLE = False
    IMPORT_ERROR = e

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

QUEUE_DIR = os.path.dirname(os.path.abspath(__file__))

_client_cache = None
_worksheet_cache = {}


def _invalidate_cache():
    global _client_cache, _worksheet_cache
    _client_cache = None
    _worksheet_cache = {}


def _get_credentials(client_file, token_file):
    creds = None
    if os.path.isfile(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def _get_worksheet(spreadsheet_id, tab_name, client_file, token_file):
    global _client_cache
    cache_key = (spreadsheet_id, tab_name)
    if cache_key in _worksheet_cache:
        return _worksheet_cache[cache_key]
    if _client_cache is None:
        creds = _get_credentials(client_file, token_file)
        _client_cache = gspread.authorize(creds)
    sh = _client_cache.open_by_key(spreadsheet_id)
    ws = sh.worksheet(tab_name)
    _worksheet_cache[cache_key] = ws
    return ws


def _write_row(spreadsheet_id, tab_name, row, client_file, token_file):
    try:
        ws = _get_worksheet(spreadsheet_id, tab_name, client_file, token_file)
        ws.insert_row(row, index=2, value_input_option="USER_ENTERED")
    except Exception as e:
        print(f"* Error writing to Google Sheet (tab '{tab_name}'): {e}")
        _invalidate_cache()
        return False

    # Inserted rows inherit the number format of whichever row they push down, so a single
    # badly-formatted row (e.g. one that picked up a date+time format instead of date-only)
    # keeps propagating that format onto every row inserted above it from then on. Explicitly
    # re-pin column A's format on every write so that chain can never take hold. Best-effort:
    # a formatting hiccup here shouldn't mark the row itself as failed/queued, since the data
    # is already safely written.
    try:
        ws.format("A2:A2", {"numberFormat": {"type": "DATE", "pattern": "M/d/yyyy"}})
    except Exception as e:
        print(f"* Warning: wrote row to Google Sheet (tab '{tab_name}') but failed to fix date format: {e}")

    return True


def _queue_file(err_code):
    return os.path.join(QUEUE_DIR, f"spreadsheet_queue_{err_code}.jsonl")


def _queue_length(err_code):
    path = _queue_file(err_code)
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def _enqueue(err_code, row):
    with open(_queue_file(err_code), "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def _drain_queue(spreadsheet_id, tab_name, err_code, client_file, token_file):
    """Attempts to write all queued rows in order, oldest first. Stops at the first
    failure so remaining rows stay queued in their original order. Returns True if the
    queue is fully empty afterwards."""
    path = _queue_file(err_code)
    if not os.path.isfile(path):
        return True

    with open(path, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]

    remaining = list(lines)
    for line in lines:
        row = json.loads(line)
        if _write_row(spreadsheet_id, tab_name, row, client_file, token_file):
            remaining.pop(0)
        else:
            break

    if remaining:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(remaining)
    else:
        os.remove(path)

    return not remaining


def update_spreadsheet(err_code, spreadsheet_id, tab_name, row, client_file, token_file):
    """
    Writes `row` to the given spreadsheet tab, draining any previously queued rows first.

    Returns (success, entered_error, recovered):
      success       - True if `row` is now live in the sheet, False if it was queued.
      entered_error - True only on the call where the queue goes from empty to non-empty.
      recovered     - True only on the call where a previously non-empty queue fully drains.
    """
    if not LIBS_AVAILABLE:
        print(f"* Error: Google Sheets libraries not installed ({IMPORT_ERROR}); queuing row.\n"
              f"    To install, run: pip install gspread google-auth-oauthlib")
        had_queue = _queue_length(err_code) > 0
        _enqueue(err_code, row)
        return False, not had_queue, False

    had_queue = _queue_length(err_code) > 0
    recovered = False

    if had_queue:
        if _drain_queue(spreadsheet_id, tab_name, err_code, client_file, token_file):
            recovered = True
            had_queue = False

    if not had_queue:
        if _write_row(spreadsheet_id, tab_name, row, client_file, token_file):
            return True, False, recovered
        _enqueue(err_code, row)
        return False, True, recovered

    # Queue still has older rows pending after the drain attempt - keep FIFO order intact
    # rather than trying (and likely failing) the current row out of order.
    _enqueue(err_code, row)
    return False, False, recovered
