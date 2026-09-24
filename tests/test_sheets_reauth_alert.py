"""
Regression tests for sheets_helper.py's on_reauth_required callback - the hook that lets
spotify_monitor.py alert (email/ntfy) right before a Google Sheets write would otherwise block
silently on interactive browser OAuth consent (flow.run_local_server()).

Real production bug: the proactive startup check (credentials_need_reauth() + a manual
alert-then-interactive_reauth() call in spotify_monitor.py) only ever caught a token that was
*already* dead before the run started. A refresh token can just as easily die mid-run (revoked,
or expired from months of inactivity) - and every mid-run write path (_get_worksheet() ->
_get_credentials(), reached from update_spreadsheet_row() or a queued-row retry) fell straight
into flow.run_local_server() with zero alerting, leaving an unattended run sitting silently
blocked in the log with nobody aware it was waiting.

These tests don't touch spotify_monitor.py's own alert_sheets_reauth_required() - that's just two
already-covered primitives (send_email/send_notification) gated on ERROR_NOTIFICATION, nothing new
to verify there. What's new here is that sheets_helper actually invokes the callback at the right
moment (once, before blocking - never after, never when no interactive consent is actually
needed), and that every public entry point threads it all the way down to _get_credentials().
"""
import sheets_helper


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


def _stub_interactive_flow(monkeypatch, calls):
    """A fake InstalledAppFlow whose from_client_secrets_file() asserts on_reauth_required already
    fired - the whole point being that the alert must land BEFORE this, never after."""
    class FakeFlow:
        @staticmethod
        def from_client_secrets_file(client_file, scopes):
            assert calls, "on_reauth_required must fire BEFORE the interactive flow is built"
            return FakeFlow()

        def run_local_server(self, port):
            return FakeCreds()

    monkeypatch.setattr(sheets_helper, "InstalledAppFlow", FakeFlow)


def test_reauth_callback_fires_once_right_before_blocking_on_consent(monkeypatch, tmp_path):
    """No token file at all - must go straight to the interactive flow, calling
    on_reauth_required exactly once, before the flow is even built."""
    calls = []
    _stub_interactive_flow(monkeypatch, calls)
    token_file = str(tmp_path / "missing_token.json")  # deliberately does not exist

    creds = sheets_helper._get_credentials("client.json", token_file, on_reauth_required=lambda: calls.append(1))

    assert calls == [1]
    assert creds is not None


def test_reauth_callback_not_called_when_token_already_valid(monkeypatch, tmp_path):
    """A live, valid cached token must never trigger the alert - only an actual reauth does."""
    calls = []
    valid_creds = FakeCreds(valid=True)
    _stub_credentials_class(monkeypatch, valid_creds)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    creds = sheets_helper._get_credentials("client.json", str(token_file), on_reauth_required=lambda: calls.append(1))

    assert calls == []
    assert creds is valid_creds


def test_reauth_callback_not_called_when_refresh_succeeds(monkeypatch, tmp_path):
    """An expired access token with a still-good refresh token must silently refresh - no alert,
    no interactive flow - since nothing here actually needs the user's attention."""
    calls = []
    expiring_creds = FakeCreds(valid=False, expired=True, refresh_token="a-refresh-token")

    def fake_refresh(self, request):
        self.valid = True

    monkeypatch.setattr(FakeCreds, "refresh", fake_refresh)
    _stub_credentials_class(monkeypatch, expiring_creds)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    creds = sheets_helper._get_credentials("client.json", str(token_file), on_reauth_required=lambda: calls.append(1))

    assert calls == []
    assert creds is expiring_creds


def test_reauth_callback_fires_when_refresh_token_itself_is_dead(monkeypatch, tmp_path):
    """The actual bug scenario: a refresh token that dies mid-run (revoked/expired -
    invalid_grant) must still alert before falling into the interactive flow."""
    calls = []
    dead_creds = FakeCreds(valid=False, expired=True, refresh_token="a-dead-refresh-token")

    def fake_refresh(self, request):
        raise Exception("invalid_grant")

    monkeypatch.setattr(FakeCreds, "refresh", fake_refresh)
    _stub_credentials_class(monkeypatch, dead_creds)
    _stub_interactive_flow(monkeypatch, calls)
    token_file = tmp_path / "token.json"
    token_file.write_text("{}", encoding="utf-8")

    sheets_helper._get_credentials("client.json", str(token_file), on_reauth_required=lambda: calls.append(1))

    assert calls == [1]


def test_update_spreadsheet_threads_the_callback_through_to_get_credentials(monkeypatch, tmp_path):
    """Plumbing check: update_spreadsheet()'s on_reauth_required must actually reach
    _get_credentials() through _write_row()/_get_worksheet() - not get dropped anywhere in
    between. Stubs _get_credentials itself as a spy rather than going through the real Sheets API,
    and stops (via a deliberate exception) right after it, since nothing past that point is what
    this test is checking."""
    monkeypatch.setattr(sheets_helper, "QUEUE_DIR", str(tmp_path))
    sheets_helper._invalidate_cache()
    received = []

    def fake_get_credentials(client_file, token_file, on_reauth_required=None):
        received.append(on_reauth_required)
        raise RuntimeError("stop here - only checking on_reauth_required reaches _get_credentials")

    monkeypatch.setattr(sheets_helper, "_get_credentials", fake_get_credentials)

    marker = lambda: None
    sheets_helper.update_spreadsheet("TESTCODE", "sheet-id", "tab", ["2026-01-01", "text"],
                                      "client.json", "token.json", on_reauth_required=marker)

    assert received == [marker]
    sheets_helper._invalidate_cache()
