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
import time
from datetime import date as _date

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
            try:
                creds.refresh(Request())
            except Exception:
                # Refresh token itself is dead (expired/revoked, e.g. invalid_grant) rather than
                # just the access token being routinely expired - fall through to interactive
                # consent instead of propagating, since that's the whole point of this function.
                creds = None
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def credentials_need_reauth(client_file, token_file):
    """
    Best-effort check of whether the cached token can still authorize without popping an
    interactive consent screen. Only returns True when interactive browser consent will
    actually be required: no token file, a corrupt one, or a refresh attempt that failed
    (e.g. invalid_grant because the refresh token itself expired or was revoked).

    Deliberately always performs a real refresh round-trip against Google when a refresh
    token is present, rather than short-circuiting on creds.valid - that flag only reflects
    the access token's locally-cached clock-based expiry, and says nothing about whether the
    refresh token underneath still actually works. A dead/revoked refresh token can sit behind
    a still-"valid" access token until the access token happens to expire naturally, which is
    exactly the failure mode this startup check exists to catch early instead of mid-run.
    """
    if not LIBS_AVAILABLE or not os.path.isfile(token_file):
        return True
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    except Exception:
        return True
    if not creds.refresh_token:
        return not creds.valid
    try:
        creds.refresh(Request())
    except Exception:
        return True
    with open(token_file, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    return False


def interactive_reauth(client_file, token_file):
    """Forces the interactive browser consent flow and caches the resulting refresh token.
    Meant to be called proactively (e.g. at startup, after credentials_need_reauth() returns
    True) so re-authorization happens at a predictable moment instead of blocking the first
    mid-run spreadsheet write unexpectedly while nobody's watching."""
    return _get_credentials(client_file, token_file)


def queue_has_pending(err_code):
    """Whether there are rows left queued for this tab from a previous run's failures."""
    return _queue_length(err_code) > 0


def drain_queue_at_startup(spreadsheet_id, tab_name, err_code, client_file, token_file):
    """Attempts to drain any rows queued by a previous run, before the main loop starts,
    instead of waiting for the next real song/event to trigger a retry. Returns
    (drained, error_message): drained is True if the queue is now fully empty; error_message
    is the exception text from whichever row failed and stopped the drain, or None."""
    if not LIBS_AVAILABLE:
        return False, f"Google Sheets libraries not installed ({IMPORT_ERROR})"
    return _drain_queue(spreadsheet_id, tab_name, err_code, client_file, token_file)


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


# Google Sheets' serial date epoch is Dec 30, 1899 (day 0).
_SHEETS_DATE_EPOCH = _date(1899, 12, 30)


def _date_to_serial(iso_date_str):
    y, m, d = (int(part) for part in iso_date_str.split("-"))
    return (_date(y, m, d) - _SHEETS_DATE_EPOCH).days


# HTTP statuses Google's own API guidance says to back off and retry on: 429 (quota), and the
# 5xx family (a transient server-side/gateway problem - including a gateway outage page that
# comes back as HTML instead of JSON, which gspread surfaces as APIError code -1 but which still
# carries the real 5xx status on the underlying response).
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_MAX_WRITE_ATTEMPTS = 3
_RETRY_BACKOFF_SECONDS = 2  # 2s before the 2nd attempt, 4s before the 3rd


def _is_retryable(e):
    """Whether e looks like one of the transient blips Google's API explicitly expects
    clients to retry (see _RETRYABLE_STATUS_CODES), as opposed to something a retry won't
    fix (bad credentials, bad spreadsheet id, a malformed request, etc.)."""
    status_code = getattr(getattr(e, "response", None), "status_code", None)
    return status_code in _RETRYABLE_STATUS_CODES


def _write_row(spreadsheet_id, tab_name, row, client_file, token_file):
    # A single batchUpdate call that inserts the row, writes both cell values, and pins their
    # number formats all atomically - one API request instead of insert_row() + a separate
    # format() call. Sheets rows inherit the number format of whichever row they push down, so
    # without pinning the format explicitly here, a single badly-formatted row (e.g. one that
    # picked up a date+time format instead of date-only) keeps propagating onto every row
    # inserted above it forever. And collapsing this to one request matters for its own sake:
    # each extra call eats into Sheets' per-minute write quota, and a backlog of queued rows
    # draining in a burst can hit a 429 far sooner at 2-3 calls/row than at 1.
    # row[0] is expected to be an ISO "YYYY-MM-DD" date string (see update_spreadsheet_row()
    # in spotify_monitor.py) and row[1] arbitrary text.
    #
    # Transient errors (429/5xx - the routine baseline blip rate of any cloud API, not anything
    # specific to this being the first write of a run) are retried inline with a short backoff
    # before falling back to the queue, so a 2-6 second Google-side hiccup resolves silently
    # instead of triggering a full queue+alert+email cycle.
    last_error = None
    for attempt in range(_MAX_WRITE_ATTEMPTS):
        try:
            ws = _get_worksheet(spreadsheet_id, tab_name, client_file, token_file)
            date_serial = _date_to_serial(row[0])
            ws.spreadsheet.batch_update({
                "requests": [
                    {
                        "insertDimension": {
                            "range": {"sheetId": ws.id, "dimension": "ROWS", "startIndex": 1, "endIndex": 2},
                            "inheritFromBefore": False,
                        }
                    },
                    {
                        "updateCells": {
                            "range": {"sheetId": ws.id, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 2},
                            "rows": [{
                                "values": [
                                    {
                                        "userEnteredValue": {"numberValue": date_serial},
                                        "userEnteredFormat": {"numberFormat": {"type": "DATE", "pattern": "M/d/yyyy"}},
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": row[1]},
                                        "userEnteredFormat": {"numberFormat": {"type": "TEXT"}},
                                    },
                                ]
                            }],
                            "fields": "userEnteredValue,userEnteredFormat.numberFormat",
                        }
                    },
                ]
            })
            return True, None
        except Exception as e:
            last_error = e
            if attempt < _MAX_WRITE_ATTEMPTS - 1 and _is_retryable(e):
                delay = _RETRY_BACKOFF_SECONDS * (attempt + 1)
                print(f"* Google Sheet write to tab '{tab_name}' hit a transient error ({e}) - retrying in {delay}s (attempt {attempt + 2}/{_MAX_WRITE_ATTEMPTS})...")
                time.sleep(delay)
                continue
            break

    print(f"* Error writing to Google Sheet (tab '{tab_name}'): {last_error}")
    _invalidate_cache()
    return False, str(last_error)


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
    failure so remaining rows stay queued in their original order. Returns
    (drained, error_message): drained is True if the queue is fully empty afterwards;
    error_message is the exception text from whichever row failed and stopped the drain
    (None if nothing failed)."""
    path = _queue_file(err_code)
    if not os.path.isfile(path):
        return True, None

    with open(path, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]

    remaining = list(lines)
    error_message = None
    for line in lines:
        row = json.loads(line)
        ok, error_message = _write_row(spreadsheet_id, tab_name, row, client_file, token_file)
        if ok:
            remaining.pop(0)
        else:
            break

    if remaining:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(remaining)
    else:
        os.remove(path)
        error_message = None

    return not remaining, error_message


def update_spreadsheet(err_code, spreadsheet_id, tab_name, row, client_file, token_file):
    """
    Writes `row` to the given spreadsheet tab, draining any previously queued rows first.

    Returns (success, entered_error, recovered, error_message):
      success       - True if `row` is now live in the sheet, False if it was queued.
      entered_error - True only on the call where the queue goes from empty to non-empty.
      recovered     - True only on the call where a previously non-empty queue fully drains.
      error_message - the exception text behind entered_error, or None.
    """
    if not LIBS_AVAILABLE:
        error_message = f"Google Sheets libraries not installed ({IMPORT_ERROR}); to install, run: pip install gspread google-auth-oauthlib"
        print(f"* Error: {error_message}; queuing row.")
        had_queue = _queue_length(err_code) > 0
        _enqueue(err_code, row)
        return False, not had_queue, False, error_message

    had_queue = _queue_length(err_code) > 0
    recovered = False

    if had_queue:
        drained, _ = _drain_queue(spreadsheet_id, tab_name, err_code, client_file, token_file)
        if drained:
            recovered = True
            had_queue = False

    if not had_queue:
        ok, error_message = _write_row(spreadsheet_id, tab_name, row, client_file, token_file)
        if ok:
            return True, False, recovered, None
        _enqueue(err_code, row)
        return False, True, recovered, error_message

    # Queue still has older rows pending after the drain attempt - keep FIFO order intact
    # rather than trying (and likely failing) the current row out of order.
    _enqueue(err_code, row)
    return False, False, recovered, None
