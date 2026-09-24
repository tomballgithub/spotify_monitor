"""
Shared harness for driving spotify_monitor_friend_uri() end-to-end against synthetic friend
data, used by test_playlist_detection_scenarios.py. Not a test module itself (no test_ prefix).

Mocks everything the monitored-playlist feature doesn't itself control: the Spotify auth token,
track/playlist metadata, the JMK_MODE hasTrack search, and outbound notifications (captured
instead of sent). Track/artist/album names are kept deliberately simple (single words, no
parentheses or brackets) so console lines can be parsed unambiguously.
"""
import contextlib
import io
import re
import time as real_time

import spotify_monitor as monitor

PLAYLIST_URI = "spotify:playlist:TESTPLAYLISTURI"
TARGET_USER_ID = "test-user"

# Matches one "now playing" console line, e.g.:
#   09/20, 12:00:00: , [03] SongB <3 - Artist (Album) [Test Playlist]*
# The [NN] bracket is minutes elapsed since the session started (time_diff_str()), not seconds -
# callers should build sequences with whole-minute spacing and assert against that same value.
_SONG_LINE_RE = re.compile(
    r"\[(?P<offset>\d+)\] "
    r"(?P<track>.+?) - (?P<artist>.+?) \((?P<album>.+?)\)"
    r"(?: \[(?P<playlist>[^\]]*)\])?(?P<icon_add>\*)?\s*$"
)
_DETECTED_LINE_RE = re.compile(r"\[(?P<offset>\d+)\] \*\*\* Playlist '(?P<name>[^']+)' Detected")
_CLEARED_LINE_RE = re.compile(r"\[(?P<offset>\d+)\] \*\*\* Playlist '(?P<name>[^']+)' Cleared")


def song(track, offset_seconds, playlist_name="", playlist_uri="", timestamp_base=None):
    """One synthetic friends-list entry: a friend playing `track` by "Artist" on album "Album",
    `offset_seconds` after `timestamp_base` (defaults to real "now" the first time this is called
    in a sequence - see build_sequence).
    """
    ts_ms = (timestamp_base + offset_seconds) * 1000
    return {
        "friends": [{
            "timestamp": ts_ms,
            "user": {"uri": f"spotify:user:{TARGET_USER_ID}", "name": "Test User"},
            "track": {
                "uri": f"spotify:track:{track}",
                "name": track,
                "artist": {"uri": "spotify:artist:artistxyz", "name": "Artist"},
                "album": {"uri": "spotify:album:albumxyz", "name": "Album"},
                "context": {"uri": playlist_uri, "name": playlist_name, "index": 0},
            },
        }],
    }


def absent():
    """A friends-list poll where the target user isn't present at all (offline/not visible)."""
    return {"friends": []}


def build_sequence(specs, step_seconds=180):
    """specs: a list of either a track name (playing "Today's Top Hits", offset auto-incremented
    by step_seconds) or a (track_name, playlist_name) tuple, or None for an `absent()` poll.
    Returns a list of friends-list JSON entries with real-"now"-based timestamps (needed since the
    monitor's inactivity checks compare against real time.time()). Anchored at real "now" (not in
    the past): since the whole sequence plays out in a fraction of a real second (time.sleep is
    mocked), a past-anchored base would make every song look stale relative to the barely-advancing
    real clock, and the friend would never appear "active" at all. Anchoring at "now" and moving
    forward instead keeps every synthetic timestamp at or after the real clock throughout the run.
    """
    base = int(real_time.time())
    entries = []
    offset = 0
    for spec in specs:
        if spec is None:
            entries.append(absent())
        else:
            track, playlist_name = spec if isinstance(spec, tuple) else (spec, "Today's Top Hits")
            playlist_uri = PLAYLIST_URI if playlist_name not in ("", "Today's Top Hits") else (
                "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M" if playlist_name == "Today's Top Hits" else ""
            )
            entries.append(song(track, offset, playlist_name, playlist_uri, timestamp_base=base))
        offset += step_seconds
    return entries


class FakeClock:
    """A controllable stand-in for time.time(), so "how much real time has passed" checks (like
    the friend-went-idle detector) can be driven deterministically instead of depending on how
    fast the test actually executes.
    """

    def __init__(self, start):
        self.value = start

    def time(self):
        return self.value


class PlaylistSession:
    """One spotify_monitor_friend_uri() run against a scripted friends-list sequence.

    friends_sequence items are normally just friends-list JSON entries (see song()/absent()), each
    served on one call to spotify_get_friends_json(). An item may instead be a (entry, clock_value)
    tuple, in which case the mocked time.time() is set to clock_value right before that entry is
    served - use this to deterministically control "how much real time has passed" checks (e.g.
    the friend-went-idle-then-active-again transition), independent of how many times time.time()
    happens to be called per polling iteration.
    """

    def __init__(self, monkeypatch, playlist_config, friends_sequence, iterations,
                 inactivity_check_seconds=60, alt_view=True, search_playlist_result=False):
        """playlist_config: a single playlist config dict (most tests - the resulting session
        tracks by session.playlist_name), or a list/tuple of them for scenarios that need more than
        one monitored playlist at once (e.g. one playlist's own "still counting up, not yet cleared"
        exception tolerance interacting with a second, different monitored playlist)."""
        self.monkeypatch = monkeypatch
        self.notifications = []
        self.output = ""
        playlist_configs = playlist_config if isinstance(playlist_config, (list, tuple)) else [playlist_config]
        self._playlist_config = playlist_configs[0]

        first_item = friends_sequence[0] if friends_sequence else None
        clock_start = first_item[1] if isinstance(first_item, tuple) else int(real_time.time())
        self.clock = FakeClock(clock_start)
        monkeypatch.setattr(monitor.time, "time", self.clock.time)

        monkeypatch.setattr(monitor, "send_email", lambda *a, **k: None)
        monkeypatch.setattr(monitor, "update_spreadsheet_row", lambda *a, **k: ("", ""))
        monkeypatch.setattr(monitor, "send_notification",
                             lambda *a, **k: self.notifications.append((a[0], a[1] if len(a) > 1 else k.get("message"))))
        monkeypatch.setattr(monitor, "spotify_get_access_token_from_sp_dc", lambda cookie: "fake-token")
        monkeypatch.setattr(monitor, "spotify_get_access_token_from_client_auto", lambda *a, **k: "fake-token")
        monkeypatch.setattr(monitor, "spotify_get_track_info", lambda access_token, track_uri: {
            "sp_artist_name": "", "sp_track_name": "", "sp_album_name": "",
            "sp_track_duration": 200, "sp_track_url": "http://x", "sp_artist_url": "http://x",
            "sp_album_url": "http://x", "sp_album_image_url": "",
        })
        monkeypatch.setattr(monitor, "spotify_get_playlist_owner_and_image",
                             lambda access_token, uri: ("Some Other User", ""))
        # True simulates Spotify's own search confirming the song really is in whatever playlist
        # it's reporting as context - used to test that a song genuinely being in the reported
        # playlist doesn't stop it from ALSO counting toward a monitored playlist it's also on.
        monkeypatch.setattr(monitor, "search_playlist", lambda *a, **k: search_playlist_result)

        monkeypatch.setattr(monitor, "JMK_MODE", True)
        monkeypatch.setattr(monitor, "ALT_VIEW", alt_view)
        monkeypatch.setattr(monitor, "TOKEN_SOURCE", "cookie")
        monkeypatch.setattr(monitor, "SP_DC_COOKIE", "fake")
        # Our mocked friends-list data never carries "sp_is_playing", so it has the shape of the
        # "buddylist" backend, not "listening_activity" (the default set by CONFIG_BLOCK's exec()
        # at import time) - activity_inactivity_check() picks SPOTIFY_LIVE_INACTIVITY_CHECK instead
        # of SPOTIFY_INACTIVITY_CHECK for the latter, silently ignoring inactivity_check_seconds.
        monkeypatch.setattr(monitor, "FRIEND_ACTIVITY_BACKEND", "buddylist")
        monkeypatch.setattr(monitor, "SPOTIFY_INACTIVITY_CHECK", inactivity_check_seconds)
        monitor.monitored_playlists_data.clear()
        for cfg in playlist_configs:
            monitor.monitored_playlists_data[cfg["name"]] = dict(cfg)
        monkeypatch.setattr(monitor, "ADD_PLAYLISTS_TO_MONITOR",
                             [monitor.monitored_playlists_data[cfg["name"]] for cfg in playlist_configs])

        import tempfile
        import os
        fd, log_path = tempfile.mkstemp(prefix="spotify_monitor_test_", suffix=".log")
        os.close(fd)
        monkeypatch.setattr(monitor, "FINAL_LOG_PATH", log_path, raising=False)
        self._log_path = log_path

        index = [0]

        def next_friends(access_token):
            i = min(index[0], len(friends_sequence) - 1)
            index[0] += 1
            item = friends_sequence[i]
            if isinstance(item, tuple):
                entry, clock_value = item
                self.clock.value = clock_value
                return entry
            return item

        monkeypatch.setattr(monitor, "spotify_get_friends_json", next_friends)

        call_count = [0]

        class _StopTest(Exception):
            pass

        def controlled_sleep(seconds):
            call_count[0] += 1
            if call_count[0] >= iterations:
                raise _StopTest()

        monkeypatch.setattr(monitor.time, "sleep", controlled_sleep)

        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                # Logger.__init__ captures sys.stdout at construction time (via
                # unwrap_terminal_stream), so it must be built *after* redirect_stdout is active,
                # or print_to_screen()'s output goes to the real terminal instead of `buf`.
                monkeypatch.setattr(monitor, "log_logger", monitor.Logger(log_path, mode="screen"), raising=False)
                monitor.spotify_monitor_friend_uri(TARGET_USER_ID, [], None)
        except _StopTest:
            pass
        finally:
            # ALT_VIEW makes the code under test reassign sys.stdout to a file-only Logger just
            # before the primary loop starts (so bare print() - e.g. "Friend got INACTIVE"/"Friend
            # got ACTIVE after being offline" - lands only in the log file, not in `buf`; only
            # print_to_screen()/print_to_both() calls write to `buf`, via the original Logger's
            # captured terminal reference). Read the log file before it's removed so those
            # log-only messages are still checkable via self.log_output.
            try:
                monitor.log_logger.logfile.close()
            except OSError:
                pass
            try:
                with open(log_path, encoding="utf-8") as f:
                    self.log_output = f.read()
            except OSError:
                self.log_output = ""
            try:
                os.remove(log_path)
            except OSError:
                pass

        self.output = buf.getvalue()

    @property
    def playlist_name(self):
        return self._playlist_config["name"]

    def song_records(self):
        """One dict per "now playing" console line: {offset, track, artist, album, playlist, icon_add}."""
        records = []
        for line in self.output.splitlines():
            m = _SONG_LINE_RE.search(line)
            if m:
                records.append({
                    "offset": int(m.group("offset")),
                    "track": m.group("track"),
                    "playlist": m.group("playlist"),  # None if no [..] tag on this line
                    "icon_add": bool(m.group("icon_add")),
                })
        return records

    def detected_offsets(self):
        return [int(m.group("offset")) for m in _DETECTED_LINE_RE.finditer(self.output)]

    def cleared_offsets(self):
        return [int(m.group("offset")) for m in _CLEARED_LINE_RE.finditer(self.output)]

    def notifications_of_type(self, kind):
        return [msg for (t, msg) in self.notifications if t == kind]
