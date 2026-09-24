"""
One additional fixture sequence, in the same shape test_fixtures.py uses, built specifically to
exercise a full detect-then-clear cycle end to end (none of the original test_fixtures.py
sequences happen to do this - they all end by repeating their last song forever, which freezes
track_changed before a clear can occur). Not part of the original test_main_loop.py/
test_fixtures.py harness - added here for run_against_target.py to demonstrate the
"Cleared" screen-line fix against the real spotify_monitor_friend_uri() loop.
"""
from test_fixtures import _friend, TARGET_USER_ID  # noqa: F401 - re-exported for run_against_target.py

# 3 on-list songs (crosses qty_start=3 -> Detected), then 2 off-list songs (crosses qty_end=2 ->
# Cleared), then back to an on-list song to show it can re-detect afterward.
SEQUENCE_DETECT_THEN_CLEAR = [
    _friend("Umbrella", "Rihanna", "Good Girl Gone Bad", "Today's Top Hits",
            "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"),
    _friend("Love On The Brain", "Rihanna", "Anti", "Today's Top Hits",
            "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", "spotify:track:3yk7PJnryiJ8mAPqsrujzf"),
    _friend("Umbrella", "Rihanna", "Good Girl Gone Bad", "Today's Top Hits",
            "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"),
    _friend("Beyond", "Leon Bridges", "Beyond", "", "", "spotify:track:5esPpmrM2AsyDVgOKzWQwU"),
    _friend("Texas Sun", "Khruangbin", "Texas Sun", "", "", "spotify:track:3k5oLgungD1dSOGLqQdIQw"),
    _friend("Love On The Brain", "Rihanna", "Anti", "Today's Top Hits",
            "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", "spotify:track:3yk7PJnryiJ8mAPqsrujzf"),
]
