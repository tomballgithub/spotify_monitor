import sys
from unittest.mock import AsyncMock, Mock

import pytest

from debug import spotify_monitor_secret_grabber as secret_grabber
from debug import spotify_monitor_totp_test as totp_test


# Verifies inline secret objects are extracted in both supported property orders
def test_extract_bundle_secrets_supports_current_object_literals():
    source = '''
    const first = {secret: "alpha", version: 61};
    const second = {"version": 62, 'secret': 'beta'};
    const duplicate = {secret: "alpha", version: 61};
    '''

    assert totp_test.extract_bundle_secrets(source) == [
        {'secret': 'alpha', 'version': 61, 'source': 'bundle'},
        {'secret': 'beta', 'version': 62, 'source': 'bundle'},
    ]


# Verifies quoted secret values use the same escape decoding as the v1.3 grabber
def test_extract_bundle_secrets_decodes_escaped_strings():
    source = r'''const item = {secret: "alpha\"beta", version: 63};'''

    assert totp_test.extract_bundle_secrets(source) == [
        {'secret': 'alpha"beta', 'version': 63, 'source': 'bundle'},
    ]


# Verifies unrelated objects are ignored by the inline secret scanner
def test_extract_bundle_secrets_ignores_nonmatching_objects():
    source = '''
    const missingVersion = {secret: "alpha"};
    const wrongType = {secret: 123, version: 64};
    const extraProperty = {secret: "beta", enabled: true, version: 65};
    '''

    assert totp_test.extract_bundle_secrets(source) == []


# Verifies token validation accepts only supported HTTPS Spotify API hosts
@pytest.mark.parametrize("url", ["https://guc-spclient.spotify.com/presence-view/v1/buddylist", "https://gew1-spclient.spotify.com/custom", "https://spclient.wg.spotify.com/path", "https://api.spotify.com/v1/me"])
def test_token_validity_url_accepts_spotify_api_hosts(url):
    assert totp_test.validate_token_validity_url(url) == url


# Verifies a custom token destination cannot exfiltrate the bearer token
@pytest.mark.parametrize("url", ["https://example.com/steal", "http://guc-spclient.spotify.com/path", "https://user@guc-spclient.spotify.com/path", "https://guc-spclient.spotify.com/path#fragment"])
def test_token_validity_url_rejects_unsafe_destinations(url):
    with pytest.raises(totp_test.argparse.ArgumentTypeError, match="HTTPS Spotify API URL"):
        totp_test.validate_token_validity_url(url)


# Verifies bearer-token validity requests cannot follow redirects
def test_token_validity_check_disables_redirects(monkeypatch):
    response = Mock(status_code=302)
    request = Mock(return_value=response)
    monkeypatch.setattr(totp_test.requests, "get", request)
    monkeypatch.setattr(totp_test, "TOKEN_VALIDITY_URL", "https://guc-spclient.spotify.com/presence-view/v1/buddylist")

    assert not totp_test.check_token_validity("token", "client", "agent")
    request.assert_called_once_with(totp_test.TOKEN_VALIDITY_URL, headers={"Authorization": "Bearer token", "Client-Id": "client", "User-Agent": "agent"}, timeout=5, allow_redirects=False)


# Verifies token utility failures produce a nonzero process result
def test_totp_utility_returns_failure_status(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["spotify_monitor_totp_test", "--sp-dc", "cookie"])
    monkeypatch.setattr(totp_test, "USER_AGENT", "agent")
    monkeypatch.setattr(totp_test, "refresh_access_token_from_sp_dc", Mock(side_effect=RuntimeError("network failure")))

    assert totp_test.main() == 1


# Verifies an invalid fetched token produces a nonzero process result
def test_totp_utility_returns_failure_for_invalid_token(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["spotify_monitor_totp_test", "--sp-dc", "cookie"])
    monkeypatch.setattr(totp_test, "USER_AGENT", "agent")
    monkeypatch.setattr(totp_test, "refresh_access_token_from_sp_dc", lambda cookie: {"access_token": "token", "expires_at": 1700000000, "client_id": "client"})
    monkeypatch.setattr(totp_test, "check_token_validity", lambda *args: False)

    assert totp_test.main() == 1


# Verifies secret extraction without usable captures produces a failure result
def test_secret_grabber_returns_failure_without_secrets(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["spotify_monitor_secret_grabber", "--secretdict"])
    monkeypatch.setattr(secret_grabber, "grab_live", AsyncMock(return_value=[]))

    assert secret_grabber.main() == 1


# Verifies output write failures propagate through the secret grabber result
def test_secret_grabber_reports_output_write_failure(monkeypatch):
    monkeypatch.setattr("builtins.open", Mock(side_effect=OSError("read-only destination")))

    assert not secret_grabber.summarise([{"secret": "alpha", "version": 61}], "all")
