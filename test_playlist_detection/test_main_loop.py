"""
Main loop test for spotify_monitor.py.

Real network traffic is used for everything EXCEPT:
  - spotify_get_friends_json() is replaced with fake data from test_fixtures.py
  - time.sleep() is shortened to MOCK_SLEEP_SECONDS
  - get_cur_ts_int() returns a future timestamp once the sequence is exhausted,
    triggering inactivity detection in the monitor

Usage:
    python test_main_loop.py

Press Ctrl+C to stop at any time.
"""

import time as _real_time
from unittest.mock import patch

# Capture real functions before any mocking happens.
_real_sleep = _real_time.sleep
_real_time_fn = _real_time.time

import spotify_monitor
from test_fixtures import TARGET_USER_ID, SEQUENCE_SONG_CHANGE, SEQUENCE_STEADY, \
    SEQUENCE_TWO_CHANGES, SEQUENCE_DISCOVERY_ZONE_DETECT, SEQUENCE_LIKED_SONGS_DETECT

# ── Configuration ──────────────────────────────────────────────────────────────

# All time.sleep() calls in the monitor will use this value instead of whatever
# the config says (which is typically 30-300 seconds).
MOCK_SLEEP_SECONDS = 0.5

# Once the sequence is exhausted, get_cur_ts_int() returns a timestamp this
# many minutes past the last track's timestamp, triggering inactivity detection.
TS_ADJUST_MINUTES = 10

FRIENDS_SEQUENCE = SEQUENCE_LIKED_SONGS_DETECT

# ── Helpers ────────────────────────────────────────────────────────────────────

def make_friends_iterator(sequence):
    """
    Returns (next_friends_fn, state) as a pair.
    state is shared with make_cur_ts_mock so it knows when the sequence ends.

    Timestamps are assigned dynamically at run time:
      - first item gets the current time in milliseconds
      - each subsequent item gets +180_000ms (3 minutes) added
    """
    import copy
    items = [copy.deepcopy(f) for f in sequence]
    now_ms = int(_real_time_fn()) * 1000
    for i, item in enumerate(items):
        for friend in item.get("friends", []):
            friend["timestamp"] = now_ms + i * 180_000

    state = {
        "exhausted": False,
        "last_ts_ms": items[-1]["friends"][0]["timestamp"] if items else now_ms,
    }
    index = [0]

    def next_friends(access_token):
        i = min(index[0], len(items) - 1)
        if index[0] >= len(items):
            state["exhausted"] = True
        index[0] += 1
        label = "repeating last" if state["exhausted"] else f"item {i + 1} of {len(items)}"
        print(f"\n[TEST] spotify_get_friends_json call #{index[0]} → {label}")
        return items[i]

    return next_friends, state


def make_cur_ts_mock(state):
    """Returns a mock for get_cur_ts_int() that returns a future timestamp once exhausted."""
    def mock_cur_ts():
        if state["exhausted"]:
            fake_ts = state["last_ts_ms"] // 1000 + TS_ADJUST_MINUTES * 60
            print(f"[TEST] get_cur_ts_int() → fake ts ({TS_ADJUST_MINUTES} mins past last track)")
            return fake_ts
        return int(_real_time_fn())
    return mock_cur_ts


def controlled_sleep(seconds):
    """Replaces time.sleep() — uses MOCK_SLEEP_SECONDS instead of the real value."""
    print(f"[TEST] time.sleep({seconds:.0f}s) → sleeping {MOCK_SLEEP_SECONDS}s instead")
    _real_sleep(MOCK_SLEEP_SECONDS)


# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[TEST] Starting monitor for user: {TARGET_USER_ID}")
    print(f"[TEST] Sequence length: {len(FRIENDS_SEQUENCE)} items (last item repeats after)")
    print(f"[TEST] Sleep duration: {MOCK_SLEEP_SECONDS}s")
    print(f"[TEST] Inactivity offset: {TS_ADJUST_MINUTES} minutes past last track timestamp")
    print(f"[TEST] Press Ctrl+C to stop\n")

    next_friends, state = make_friends_iterator(FRIENDS_SEQUENCE)
    mock_cur_ts = make_cur_ts_mock(state)

    with patch("spotify_monitor.spotify_get_friends_json", side_effect=next_friends), \
         patch("spotify_monitor.get_cur_ts_int", side_effect=mock_cur_ts), \
         patch("spotify_monitor.time.sleep", side_effect=controlled_sleep):
        try:
            # spotify_monitor.spotify_monitor_friend_uri(TARGET_USER_ID, [], None)
            spotify_monitor.main()
        except KeyboardInterrupt:
            print("\n[TEST] Stopped.")
