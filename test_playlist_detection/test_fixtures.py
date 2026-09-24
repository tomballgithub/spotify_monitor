"""
Fake spotify_get_friends_json() responses for testing spotify_monitor.py.

Each entry in a sequence is what spotify_get_friends_json() will return on
successive calls. The last entry is repeated once the list is exhausted.

Structure matches exactly what the real Spotify buddylist API returns,
confirmed from reading spotify_get_friend_info() in the source (line ~3560).
"""

import time

# The user URI ID being monitored (just the id part, no "spotify:user:" prefix)
TARGET_USER_ID = "jeoff-us"

_NOW_MS = int(time.time()) * 1000  # current time in milliseconds


def _friend(track_name, artist_name, album_name, playlist_name, playlist_uri,
            track_uri, timestamp_ms=0):
    """Build one friends-list JSON entry for TARGET_USER_ID."""
    return {
        "friends": [
            {
                "timestamp": timestamp_ms,
                "user": {
                    "uri": f"spotify:user:{TARGET_USER_ID}",
                    "name": "Test User"
                },
                "track": {
                    "uri": track_uri,
                    "name": track_name,
                    "artist": {
                        "uri": "spotify:artist:artistxyz",
                        "name": artist_name
                    },
                    "album": {
                        "uri": "spotify:album:albumxyz",
                        "name": album_name
                    },
                    "context": {
                        "uri": playlist_uri,
                        "name": playlist_name,
                        "index": 0
                    }
                }
            }
        ]
    }


# ── Individual states ──────────────────────────────────────────────────────────

# User playing "Umbrella" right now
PLAYING_UMBRELLA = _friend(
    track_name    = "Umbrella",
    artist_name   = "Rihanna",
    album_name    = "Good Girl Gone Bad",
    playlist_name = "Today's Top Hits",
    playlist_uri  = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
    track_uri     = "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
)

# User changed to "Love On The Brain" 3 minutes later.
# Different timestamp is what triggers song-change detection (sp_ts != sp_ts_old).
PLAYING_LOVE_ON_THE_BRAIN = _friend(
    track_name    = "Love On The Brain",
    artist_name   = "Rihanna",
    album_name    = "Anti",
    playlist_name = "Today's Top Hits",
    playlist_uri  = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
    track_uri     = "spotify:track:3yk7PJnryiJ8mAPqsrujzf",
)

# Same song still playing — same timestamp as above, so no song-change event fires.
# Use this to simulate the user sitting idle on the same track.
STILL_PLAYING_LOVE_ON_THE_BRAIN = _friend(
    track_name    = "Love On The Brain",
    artist_name   = "Rihanna",
    album_name    = "Anti",
    playlist_name = "Today's Top Hits",
    playlist_uri  = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
    track_uri     = "spotify:track:3yk7PJnryiJ8mAPqsrujzf",
)


# ── Sequences ──────────────────────────────────────────────────────────────────
# Pick whichever sequence matches the scenario you want to test,
# or build your own list in test_main_loop.py.

# Scenario A: user starts playing, changes song, then stays on that song
SEQUENCE_SONG_CHANGE = [
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    STILL_PLAYING_LOVE_ON_THE_BRAIN, # call 3+: no further change (last item repeats)
]

# Scenario B: user is already playing when the monitor starts, no changes
SEQUENCE_STEADY = [
    PLAYING_UMBRELLA,                # repeated on every call
]

# Scenario C: two song changes then idle
SEQUENCE_TWO_CHANGES = [
    PLAYING_UMBRELLA,
    PLAYING_LOVE_ON_THE_BRAIN,
    PLAYING_UMBRELLA,                # switches back
    STILL_PLAYING_LOVE_ON_THE_BRAIN, # sits idle after (last item repeats)
]

# ── Scenario D: real captured stream — jeoff-us playing Discovery Zone playlist ─

SEQUENCE_DISCOVERY_ZONE_DETECT = [
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    _friend(
        track_name    = "Beyond",
        artist_name   = "Leon Bridges",
        album_name    = "Beyond",
        playlist_name = "",
        playlist_uri  = "",
        track_uri     = "spotify:track:5esPpmrM2AsyDVgOKzWQwU",
    ),
    _friend(
        track_name    = "Don't Dream It's Over",
        artist_name   = "Crowded House",
        album_name    = "Crowded House",
        playlist_name = "Today's Top Hits",
        playlist_uri  = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
        track_uri     = "spotify:track:7G7tgVYORlDuVprcYHuFJh",
    ),
    _friend(
        track_name    = "Marry Me",
        artist_name   = "Train",
        album_name    = "Save Me, San Francisco (Golden Gate Edition)",
        playlist_name = "",
        playlist_uri  = "",
        track_uri     = "spotify:track:2MWOqewf5j0qf2b6S5J6cS",
    ),
    _friend(
        track_name    = "Texas Sun",
        artist_name   = "Khruangbin",
        album_name    = "Texas Sun",
        playlist_name = "",
        playlist_uri  = "",
        track_uri     = "spotify:track:3k5oLgungD1dSOGLqQdIQw",
    ),
    _friend(
        track_name    = "Heavenly Day",
        artist_name   = "Patty Griffin",
        album_name    = "Children Running Through",
        playlist_name = "",
        playlist_uri  = "",
        track_uri     = "spotify:track:2vy6F2C23RxlGJvbdA7NTq",
    ),
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    PLAYING_UMBRELLA,                # call 1: first song detected at startup

]

# ── Scenario E: real captured stream — jeoff-us playing directly from albums ───
# Note: playlist_uri is spotify:album:... not spotify:playlist:...
# This is what the API returns when the user plays from an album rather than
# a playlist. Worth testing that your script handles this correctly.

SEQUENCE_LIKED_SONGS_DETECT = [
    _friend(
        track_name    = "Umbrella",
        artist_name   = "Rihanna",
        album_name    = "Good Girl Gone Bad",
        playlist_name = "Today's Top Hits",
        playlist_uri  = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
        track_uri     = "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
        timestamp_ms  = 1777240423327,
    ),
    _friend(
        track_name    = "Amarillo By Morning",
        artist_name   = "George Strait",
        album_name    = "Strait From The Heart",
        playlist_name = "Strait From The Heart",
        playlist_uri  = "spotify:album:3NB2cmFq9nyhHSVz0Zv08t",
        track_uri     = "spotify:track:4TnUKixNWMfajncgdSwFoi",
        timestamp_ms  = 1777244112950,
    ),
    _friend(
        track_name    = "Champagne Supernova - Remastered",
        artist_name   = "Oasis",
        album_name    = "(What's The Story) Morning Glory? [Remastered]",
        playlist_name = "(What's The Story) Morning Glory? [Remastered]",
        playlist_uri  = "spotify:album:1VW1MFNstaJuygaoTPkdCk",
        track_uri     = "spotify:track:1wo3UYTeizJHkwYIuLuBPF",
        timestamp_ms  = 1777250420123,
    ),
    _friend(
        track_name    = "Lonely Tonight (feat. Ashley Monroe)",
        artist_name   = "Blake Shelton",
        album_name    = "Reloaded: 20 #1 Hits",
        playlist_name = "Reloaded: 20 #1 Hits",
        playlist_uri  = "spotify:album:0ujKXmDetsmfjNvmwW546y",
        track_uri     = "spotify:track:3KNtQ1twm53HpEzebdfvgm",
        timestamp_ms  = 1777250463962,
    ),
    _friend(
        track_name    = "I'm Yours",
        artist_name   = "Brandon Myles",
        album_name    = "Piano Covers: 00s Hits",
        playlist_name = "Piano Covers: 00s Hits",
        playlist_uri  = "spotify:album:2nA56L3wTiYZEwKQbi0QkO",
        track_uri     = "spotify:track:71yVvoFawU7TOsk2MKu0MJ",
        timestamp_ms  = 1777250643347,
    ),
    _friend(
        track_name    = "Rap God",
        artist_name   = "Eminem",
        album_name    = "The Marshall Mathers LP2 (Deluxe)",
        playlist_name = "The Marshall Mathers LP2 (Deluxe)",
        playlist_uri  = "spotify:album:6DN7GcZF1HywzrkGN6Eeqk",
        track_uri     = "spotify:track:6or1bKJiZ06IlK0vFvY75k",
        timestamp_ms  = 1777250721667,
    ),
    _friend(
        track_name    = "See You Again (feat. Charlie Puth)",
        artist_name   = "Wiz Khalifa",
        album_name    = "See You Again (feat. Charlie Puth)",
        playlist_name = "See You Again (feat. Charlie Puth)",
        playlist_uri  = "spotify:album:02tTjKlh9iQ5jlWYPbKLJZ",
        track_uri     = "spotify:track:7wqSzGeodspE3V6RBD5W8L",
        timestamp_ms  = 1777250952503,
    ),
    _friend(
        track_name    = 'Doin\' The Do - 7" Radio Mix',
        artist_name   = "Betty Boo",
        album_name    = "Boomania",
        playlist_name = "Boomania",
        playlist_uri  = "spotify:album:6945nocZM0gGU8U9IG0gzp",
        track_uri     = "spotify:track:3h9mCACYWP4iDVFEBhyyYC",
        timestamp_ms  = 1777251175506,
    ),
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
    PLAYING_LOVE_ON_THE_BRAIN,       # call 2: song changes
    PLAYING_UMBRELLA,                # call 1: first song detected at startup
]
