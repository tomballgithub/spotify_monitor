"""
Regression tests for sheets_helper.py's Google Sheets reauth callbacks - the hooks that let
spotify_monitor.py narrate (and, when it matters, alert on email/ntfy) what's happening right
before a Google Sheets write would otherwise block silently on interactive browser OAuth consent
(flow.run_local_server()).

Real production bug #1: the proactive startup check (credentials_need_reauth() + a manual
alert-then-interactive_reauth() call in spotify_monitor.py) only ever caught a token that was
*already* dead before the run started. A refresh token can just as easily die mid-run (revoked,
or expired from months of inactivity) - and every mid-run write path (_get_worksheet() ->
_get_credentials(), reached from update_spreadsheet_row() or a queued-row retry) fell straight
into flow.run_local_server() with zero alerting, leaving an unattended run sitting silently
blocked in the log with nobody aware it was waiting.

Real production bug #2: Google can silently reissue a code - no visible consent screen, no click -
when the account has already granted this app+scope before and its browser session is already
signed in. Watching this happen live ("authorization needed... opening browser for consent" then
"authorization complete", with no browser ever visibly appearing) looked exactly like the script
had approved something on its own, when really Google's server made that call, not spotify_monitor.
_get_credentials() now runs flow.run_local_server() in a background thread and gives it a short
grace period: on_checking() always fires first, then either on_reauth_silent() (finished within the
grace period - nothing needed anyone's attention, no alert) or on_reauth_required(auth_url) (still
running past it - alert for real, with the actual authorization URL, since a real person can't
plausibly see a page and click Allow within a few seconds). auth_url itself is captured by patching
webbrowser.get() (real_local_server() calls .open() on what that returns, not webbrowser.open()
directly), rather than building a second authorization_url() ourselves, which would carry a
different state than the one the local callback server is actually listening for.

These tests don't touch spotify_monitor.py's own alert_sheets_reauth_required()/_silent()/
_checking() bodies beyond confirming their content - those are just string formatting plus two
already-covered primitives (send_email/send_notification) gated on ERROR_NOTIFICATION. What's new
here is that sheets_helper invokes exactly one of on_reauth_silent()/on_reauth_required(url) per
pass (never both, always after on_checking()), based on real elapsed time against a patched grace
period, and that every public entry point threads all three callbacks down to _get_credentials().
"""
import time
import webbrowser

import pytest

import sheets_helper
import spotify_monitor as monitor


class FakeCreds:
    def __init__(self, valid=True, expired=False, refresh_token=None):
        self.valid = valid
        self.expired = expired
        self.refresh_token = refresh_token

    def refresh(self, request):
        pass

    def to_json(self):
        return "{}"


def _stub_credentials_class(monkeypatch, cached_creds):
    """Swaps sheets_helper's own `Credentials` name (not the real google-auth class) so
    Credentials.from_authorized_user_file(...) returns whatever this test wants, without touching
    real library internals."""
    class FakeCredentialsClass:
        @staticmethod
        def from_authorized_user_file(path, scopes):
            return cached_creds

    monkeypatch.setattr(sheets_helper, "Credentials", FakeCredentialsClass)


class FakeBrowserController:
    """Stands in for whatever webbrowser.get(browser) would normally return - real
    run_local_server() calls .open() on exactly this kind of object, not webbrowser.open()."""

    def __init__(self):
        self.opened = []

    def open(self, url, *args, **kwargs):
        self.opened.append(url)
        return True


# Real grace period is 5s - tests patch it down to this so "still running past the grace period"
# tests take a fraction of a second instead of 5+.
_TEST_GRACE_SECONDS = 0.05


def _stub_interactive_flow(monkeypatch, delay_seconds, auth_url="https://accounts.google.com/o/oauth2/auth?fake=1"):
    """A fake InstalledAppFlow whose run_local_server() opens a browser the same way the real one
    does (via webbrowser.get(...).open(auth_url, ...)), so sheets_helper's own webbrowser.get()
    patch has something real to intercept, then blocks for delay_seconds before "completing" -
    standing in for however long Google actually takes to redirect back (near-instant for a silent
    reissue, or however long a real person takes to click through, for a genuine one)."""
    monkeypatch.setattr(sheets_helper, "_SILENT_REAUTH_GRACE_SECONDS", _TEST_GRACE_SECONDS)
    monkeypatch.setattr(webbrowser, "get", lambda using=None: FakeBrowserController())

    class FakeFlow:
        @staticmethod
        def from_client_secrets_file(client_file, scopes):
            return FakeFlow()

        def run_local_server(self, port):
            webbrowser.get(None).open(auth_url, new=1, autoraise=True)
            time.sleep(delay_seconds)
            return FakeCreds()

    monkeypatch.setattr(sheets_helper, "InstalledAppFlow", FakeFlow)


def test_checking_fires_first_and_silent_fires_when_the_flow_finishes_within_the_grace_period(monkeypatch, tmp_path):
    """The common case: Google reissues near-instantly (already-granted app+scope, already-signed-in
    browser). on_checking() must fire, then on_reauth_silent() - never on_reauth_required(), since
    nothing here needs anyone's attention."""
    events = []
    _stub_interactive_flow(monkeypatch, delay_seconds=0)
    token_file = str(tmp_path / "missing_token.json")  # deliberately does not exist

    creds = sheets_helper._get_credentials(
        "client.json", token_file,
        on_checking=lambda: events.append("checking"),
        on_reauth_silent=lambda: events.append("silent"),
        on_reauth_required=lambda url: events.append(("required", url)),
    )

    assert events == ["checking", "silent"]
    assert creds is not None


def test_required_fires_with_the_real_url_when_the_flow_outlasts_the_grace_period(monkeypatch, tmp_path):
    """The actual bug scenario made visible: a flow that's still running once the grace period
    elapses is genuinely waiting on a person - on_reauth_required(auth_url) must fire, with the
    real URL run_local_server() is using, and on_reauth_silent() must not fire at all."""
    events = []
    _stub_interactive_flow(monkeypatch, delay_seconds=_TEST_GRACE_SECONDS * 4,
                            auth_url="https://accounts.google.com/o/oauth2/auth?fake=needs-a-person")
    token_file = str(tmp_path / "missing_token.json")

    creds = sheets_helper._get_credentials(
        "client.json", token_file,
        on_checking=lambda: events.append("checking"),
        on_reauth_silent=lambda: events.append("silent"),
        on_reauth_required=lambda url: events.append(("required", url)),
    )

    assert events == ["checking", ("required", "https://accounts.google.com/o/oauth2/auth?fake=needs-a-person")]
    assert creds is not None


def test_reauth_callback_not_called_when_token_already_valid(monkeypatch, tmp_path):
    """A live, valid cached token must never trigger any of the three callbacks - only an actual
    reauth attempt does."""
    events = []
    valid_creds = FakeCreds(valid=True)
    _stub_credentials_class(monkeypatch, valid_creds)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    creds = sheets_helper._get_credentials(
        "client.json", str(token_file),
        on_checking=lambda: events.append("checking"),
        on_reauth_silent=lambda: events.append("silent"),
        on_reauth_required=lambda url: events.append(("required", url)),
    )

    assert events == []
    assert creds is valid_creds


def test_reauth_callback_not_called_when_refresh_succeeds(monkeypatch, tmp_path):
    """An expired access token with a still-good refresh token must silently refresh via the
    ordinary (non-interactive) refresh path - no callback of any kind, since nothing here ever
    touches run_local_server() at all."""
    events = []
    expiring_creds = FakeCreds(valid=False, expired=True, refresh_token="a-refresh-token")

    def fake_refresh(self, request):
        self.valid = True

    monkeypatch.setattr(FakeCreds, "refresh", fake_refresh)
    _stub_credentials_class(monkeypatch, expiring_creds)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    creds = sheets_helper._get_credentials(
        "client.json", str(token_file),
        on_checking=lambda: events.append("checking"),
        on_reauth_silent=lambda: events.append("silent"),
        on_reauth_required=lambda url: events.append(("required", url)),
    )

    assert events == []
    assert creds is expiring_creds


def test_reauth_reaches_the_interactive_flow_when_the_refresh_token_itself_is_dead(monkeypatch, tmp_path):
    """The other real bug scenario: a refresh token that dies mid-run (revoked/expired -
    invalid_grant) must still fall into the interactive flow, not silently give up."""
    events = []
    dead_creds = FakeCreds(valid=False, expired=True, refresh_token="a-dead-refresh-token")

    def fake_refresh(self, request):
        raise Exception("invalid_grant")

    monkeypatch.setattr(FakeCreds, "refresh", fake_refresh)
    _stub_credentials_class(monkeypatch, dead_creds)
    _stub_interactive_flow(monkeypatch, delay_seconds=0)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    sheets_helper._get_credentials(
        "client.json", str(token_file),
        on_checking=lambda: events.append("checking"),
        on_reauth_silent=lambda: events.append("silent"),
        on_reauth_required=lambda url: events.append(("required", url)),
    )

    assert events == ["checking", "silent"]


def test_exception_in_the_background_flow_propagates_to_the_caller(monkeypatch, tmp_path):
    """run_local_server() failing (e.g. a real network error) must still surface as a real
    exception to the caller - running it in a background thread for the grace-period timing must
    not swallow it."""
    monkeypatch.setattr(sheets_helper, "_SILENT_REAUTH_GRACE_SECONDS", _TEST_GRACE_SECONDS)
    monkeypatch.setattr(webbrowser, "get", lambda using=None: FakeBrowserController())

    class FailingFlow:
        @staticmethod
        def from_client_secrets_file(client_file, scopes):
            return FailingFlow()

        def run_local_server(self, port):
            raise RuntimeError("network unreachable")

    monkeypatch.setattr(sheets_helper, "InstalledAppFlow", FailingFlow)
    token_file = str(tmp_path / "missing_token.json")

    with pytest.raises(RuntimeError, match="network unreachable"):
        sheets_helper._get_credentials("client.json", token_file)


def test_update_spreadsheet_threads_all_three_callbacks_through_to_get_credentials(monkeypatch, tmp_path):
    """Plumbing check: update_spreadsheet()'s on_checking/on_reauth_silent/on_reauth_required must
    all actually reach _get_credentials() through _write_row()/_get_worksheet() - not get dropped
    anywhere in between. Stubs _get_credentials itself as a spy rather than going through the real
    Sheets API, and stops (via a deliberate exception) right after it, since nothing past that
    point is what this test is checking."""
    monkeypatch.setattr(sheets_helper, "QUEUE_DIR", str(tmp_path))
    sheets_helper._invalidate_cache()
    received = []

    def fake_get_credentials(client_file, token_file, on_checking=None, on_reauth_silent=None, on_reauth_required=None):
        received.append((on_checking, on_reauth_silent, on_reauth_required))
        raise RuntimeError("stop here - only checking the callbacks reach _get_credentials")

    monkeypatch.setattr(sheets_helper, "_get_credentials", fake_get_credentials)

    checking_marker = lambda: None
    silent_marker = lambda: None
    required_marker = lambda url: None
    sheets_helper.update_spreadsheet("TESTCODE", "sheet-id", "tab", ["2026-01-01", "text"],
                                      "client.json", "token.json",
                                      on_checking=checking_marker, on_reauth_silent=silent_marker,
                                      on_reauth_required=required_marker)

    assert received == [(checking_marker, silent_marker, required_marker)]
    sheets_helper._invalidate_cache()


def test_capturing_browser_controller_still_opens_the_real_browser():
    """The interception must be transparent: capturing the URL can't come at the cost of the real
    browser launch users still rely on when they're at the machine."""
    real = FakeBrowserController()
    captured = {}
    controller = sheets_helper._CapturingBrowserController(real, captured)

    result = controller.open("https://example.com/authorize", new=1, autoraise=True)

    assert captured == {"url": "https://example.com/authorize"}
    assert real.opened == ["https://example.com/authorize"]
    assert result is True


def test_webbrowser_get_is_restored_after_the_interactive_flow(monkeypatch, tmp_path):
    """The patch to webbrowser.get() is process-global for the duration of the call - it must not
    leak into whatever runs after, or every later webbrowser.get() call in the process (including
    an unrelated one, e.g. scrobble health's own OAuth flow) would silently start being captured
    too."""
    _stub_interactive_flow(monkeypatch, delay_seconds=0)
    original_get = webbrowser.get
    token_file = str(tmp_path / "missing_token.json")

    sheets_helper._get_credentials("client.json", token_file)

    assert webbrowser.get is original_get


def test_alert_sheets_reauth_required_includes_a_clickable_link(monkeypatch):
    """spotify_monitor.py's own alert must embed the real authorization URL sheets_helper hands
    it, as a clickable link in the HTML body and a plain one in the text body - the whole point
    of threading auth_url through was to spare the user from having to be at the machine to see
    it, or to hunt for it in the log if the automatic browser launch silently failed."""
    monkeypatch.setattr(monitor, "ERROR_NOTIFICATION", True)
    monkeypatch.setattr(monitor, "ERR_CODE", "JMK")
    sent_emails = []
    monkeypatch.setattr(monitor, "send_email", lambda subject, body, body_html, use_ssl: sent_emails.append((subject, body, body_html)))
    monkeypatch.setattr(monitor, "send_notification", lambda *args, **kwargs: None)

    monitor.alert_sheets_reauth_required("https://accounts.google.com/o/oauth2/auth?fake=1&state=abc")

    assert len(sent_emails) == 1
    subject, body, body_html = sent_emails[0]
    assert "JMK" in subject
    assert "https://accounts.google.com/o/oauth2/auth?fake=1&state=abc" in body
    assert 'href="https://accounts.google.com/o/oauth2/auth?fake=1&amp;state=abc"' in body_html


def test_alert_sheets_reauth_required_omits_the_link_section_without_a_url(monkeypatch):
    """No URL available (e.g. a caller that hasn't been updated, or a future code path that can't
    get one) must not print a broken/empty link line - the whole section is left out instead."""
    monkeypatch.setattr(monitor, "ERROR_NOTIFICATION", True)
    monkeypatch.setattr(monitor, "ERR_CODE", "JMK")
    sent_emails = []
    monkeypatch.setattr(monitor, "send_email", lambda subject, body, body_html, use_ssl: sent_emails.append((subject, body, body_html)))
    monkeypatch.setattr(monitor, "send_notification", lambda *args, **kwargs: None)

    monitor.alert_sheets_reauth_required()

    subject, body, body_html = sent_emails[0]
    assert "Authorization link" not in body
    assert "Authorization link" not in body_html


def test_alert_sheets_reauth_silent_and_checking_never_send_email_or_ntfy(monkeypatch):
    """The whole point of splitting these out: a routine, unattended-safe outcome (still checking,
    or a silent reissue) must never fire an alert that has nothing to actually tell anyone to do -
    only alert_sheets_reauth_required() (a person is genuinely needed) does."""
    monkeypatch.setattr(monitor, "ERROR_NOTIFICATION", True)
    monkeypatch.setattr(monitor, "ERR_CODE", "JMK")
    monkeypatch.setattr(monitor, "send_email", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not send email")))
    monkeypatch.setattr(monitor, "send_notification", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not send a push notification")))

    monitor.alert_sheets_reauth_checking()
    monitor.alert_sheets_reauth_silent()
