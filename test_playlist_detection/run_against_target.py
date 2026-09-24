"""
Runs test_main_loop.py's mocked friends-list sequences (from test_fixtures.py) against a given
spotify_monitor.py, calling spotify_monitor_friend_uri() directly for a bounded number of
iterations instead of the open-ended main() loop test_main_loop.py itself drives.

Everything test_main_loop.py already mocks (the friends-list poll, time.sleep, the inactivity
clock) is mocked the same way here. This script additionally stubs out the calls neither
test_main_loop.py nor test_fixtures.py mock - the Spotify auth token, track/playlist metadata,
the JMK_MODE hasTrack search, and every outbound notification (email/push/spreadsheet) - so it
runs fully offline and side-effect-free without real Spotify credentials. That's a deliberate
difference from test_main_loop.py's own intent (which says "Real network traffic is used for
everything EXCEPT..." - i.e. it's meant to be run with real credentials for manual, live
verification); this script exists for automated, repeatable comparison instead.

It also seeds one synthetic monitored playlist ("Test Playlist", containing "Umbrella" and
"Love On The Brain" by Rihanna, both of which already appear in every fixture sequence) so the
detection/clearing logic has something real to match against.

Usage:
    python run_against_target.py <path-to-spotify_monitor.py-directory> <SEQUENCE_NAME> <num_iterations> [output_file]

Example:
    python run_against_target.py .. SEQUENCE_DISCOVERY_ZONE_DETECT 12
    python run_against_target.py "C:\\Python Dev\\spotify_monitor" SEQUENCE_DISCOVERY_ZONE_DETECT 12
"""
import contextlib
import importlib.util
import io
import os
import sys
import tempfile

if len(sys.argv) < 4:
    print(__doc__)
    raise SystemExit(1)

target_dir = os.path.abspath(sys.argv[1])
sequence_name = sys.argv[2]
n_iters = int(sys.argv[3])
out_path = sys.argv[4] if len(sys.argv) > 4 else None

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)  # test_fixtures.py / test_main_loop.py live alongside this script

spec = importlib.util.spec_from_file_location("sm_under_test", os.path.join(target_dir, "spotify_monitor.py"))
sm = importlib.util.module_from_spec(spec)
sys.modules["sm_under_test"] = sm
sys.modules["spotify_monitor"] = sm  # test_fixtures.py / test_main_loop.py do `import spotify_monitor`
spec.loader.exec_module(sm)

import test_fixtures as fx  # noqa: E402
import demo_fixtures as demo  # noqa: E402 - extra sequences not in the original test_fixtures.py
import test_main_loop as tml  # noqa: E402 - guarded by `if __name__ == "__main__":`, safe to import

sequence = getattr(fx, sequence_name, None) or getattr(demo, sequence_name)
make_friends_iterator = tml.make_friends_iterator

# ---- Stub every side-effecting / network call the fixtures themselves don't mock ----
sm.send_email = lambda *a, **k: None
sm.update_spreadsheet_row = lambda *a, **k: ("", "")
sent_notifications = []
sm.send_notification = lambda *a, **k: sent_notifications.append((a[0], a[1] if len(a) > 1 else k.get("message")))

sm.spotify_get_access_token_from_sp_dc = lambda cookie: "fake-token"
sm.spotify_get_access_token_from_client_auto = lambda *a, **k: "fake-token"


def fake_track_info(access_token, track_uri):
    return {
        "sp_artist_name": "", "sp_track_name": "", "sp_album_name": "",
        "sp_track_duration": 200, "sp_track_url": "http://x", "sp_artist_url": "http://x",
        "sp_album_url": "http://x", "sp_album_image_url": "",
    }


sm.spotify_get_track_info = fake_track_info
sm.spotify_get_playlist_owner_and_image = lambda access_token, uri: ("Some Other User", "")
sm.search_playlist = lambda *a, **k: False  # let PlaylistTracker's own matching decide "hasTrack" instead

# ---- Config: enable the custom monitored-playlist feature and seed one playlist ----
sm.JMK_MODE = True
sm.ALT_VIEW = True
sm.TOKEN_SOURCE = "cookie"
sm.SP_DC_COOKIE = "fake"
scratch_log_fd, sm.FINAL_LOG_PATH = tempfile.mkstemp(prefix="spotify_monitor_test_", suffix=".log")
os.close(scratch_log_fd)
sm.log_logger = sm.Logger(sm.FINAL_LOG_PATH, mode="screen")
sm.monitored_playlists_data.clear()
sm.monitored_playlists_data["Test Playlist"] = {
    # qty_start/qty_end match the real Discovery Zone config's defaults (3 in a row to detect,
    # 2 in a row off-list to clear), so results here read the same way your real logs do.
    'name': "Test Playlist", 'filename': "", 'qty_start': 3, 'qty_end': 2,
    'url': 'http://playlist', 'icon': ' <3', 'notify': True, 'override': False, 'refresh': 0,
    'tracks_set': {"RIHANNA - UMBRELLA", "RIHANNA - LOVE ON THE BRAIN"},
    'count_start': 0, 'count_end': 0, 'count_shuffle': 0,
}
sm.ADD_PLAYLISTS_TO_MONITOR = [sm.monitored_playlists_data["Test Playlist"]]

# ---- Friends-list + clock mocks, exactly like test_main_loop.py's own ----
next_friends, state = make_friends_iterator(sequence)
sm.spotify_get_friends_json = lambda access_token: next_friends(access_token)

call_count = [0]


class StopTest(Exception):
    pass


def controlled_sleep(seconds):
    call_count[0] += 1
    if call_count[0] >= n_iters:
        raise StopTest()


sm.time.sleep = controlled_sleep

buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        sm.spotify_monitor_friend_uri(fx.TARGET_USER_ID, [], None)
except StopTest:
    pass
except Exception as e:
    print(f"[RUNNER] Stopped by exception: {type(e).__name__}: {e}", file=sys.stderr)

try:
    sm.log_logger.logfile.close()
    os.remove(sm.FINAL_LOG_PATH)
except OSError:
    pass

output = buf.getvalue()
if out_path:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
else:
    print(output.encode("ascii", "replace").decode("ascii"))

print("=" * 80)
print(f"[RUNNER] {sequence_name} against {target_dir}: {call_count[0]} sleep/iterations, "
      f"{len(sent_notifications)} notification(s) sent")
for n in sent_notifications:
    print(f"    notification: type={n[0]!r} message={n[1]!r}")
tp = sm.monitored_playlists_data["Test Playlist"]
print(f"    final Test Playlist state: count_start={tp['count_start']} count_end={tp['count_end']} count_shuffle={tp['count_shuffle']}")
