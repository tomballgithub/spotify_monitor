# Playlist Detection Test Information

This is the in-depth reference for `test_playlist_detection_scenarios.py` - the automated pytest
suite for the monitored-playlist detection feature (`PlaylistTracker` / `ADD_PLAYLISTS_TO_MONITOR`
/ `validate_add_playlists_to_monitor()` in `spotify_monitor.py`). The source file's own comments
are intentionally brief; this document exists to spell out, for every test, **what real-world
situation it's standing in for, what behavior it's checking, and why that behavior is the correct
one** - not just the mechanics of the assertion. It's a reference for revisiting this suite later,
not something pytest reads - if you change the detection algorithm, this is the file to re-derive
expectations from.

Related files:
- **`test_playlist_detection_scenarios.py`** - the 42 tests themselves.
- **`playlist_harness.py`** - the shared harness these tests drive (`PlaylistSession`, `song()`,
  `build_sequence()`, `absent()`, `FakeClock`). See "How the harness works" below.
- **`../test_playlist_detection/README.md`** - a separate, *manual* comparison harness (diffs this
  codebase's output against another one, e.g. the pre-refactor original). Not run by pytest.

## The feature, in plain terms

You give the monitor a list of playlists to watch for (`ADD_PLAYLISTS_TO_MONITOR`) - for example,
your Discovery Zone or Liked Songs. Each entry names a text file of "artist - track" lines that
belong to that playlist, plus a few numbers:

- **`qty_start`** - how many songs *in a row* from that list it takes before the tool decides "the
  friend is listening to this playlist" and announces **Detected**.
- **`qty_end`** - how many songs *in a row* **not** on the list it takes before the tool decides
  "they've moved on" and announces **Cleared**. Because Spotify's own shuffle sometimes slips in a
  song that isn't technically on your saved list, up to `qty_end - 1` off-list songs in a row are
  quietly tolerated (a "smart shuffle exception") once the playlist has already been detected -
  only the `qty_end`-th one in a row actually clears it.
- **`icon`** - an optional marker (e.g. `" <3"` or `" ♥"`) appended to the track name whenever a
  song is confirmed on the playlist, so it's visually obvious at a glance in the console/log.
- **`override`** - if the friend might already be partway through the playlist *before* you started
  monitoring, this lets the very first observed song count as an instant match instead of making
  you wait through `qty_start` more songs to notice something that was already true.
- **`notify`** - whether crossing these thresholds should send a real notification (email/push/etc),
  independent of whether it shows up on screen.

Every observed song runs through `PlaylistTracker.advance()`, which decides one of three outcomes:
the song **extends** a playlist's streak (confirmed match), the song is a **tolerated exception**
(counts toward `qty_end` but doesn't break the streak yet), or the song **has nothing to do with**
any monitored playlist right now. This test suite exists to pin down, precisely, when each of those
three outcomes happens - and to make sure the on-screen tag, the shuffle icon, and the
Detected/Cleared announcements only ever appear exactly where they should.

## How the harness works

`PlaylistSession(monkeypatch, playlist_config, friends_sequence, iterations, ...)` drives the real
`spotify_monitor_friend_uri()` loop end-to-end against synthetic data - not a unit test of
`PlaylistTracker` in isolation, but the actual production code path, with only network/notification
calls mocked out.

- **`song(track, offset_seconds, playlist_name, playlist_uri, timestamp_base)`** builds one
  synthetic "friend is listening to X" API response. Artist is always `"Artist"`, album always
  `"Album"` - kept simple so console lines parse unambiguously.
- **`search_playlist_result`** (on `PlaylistSession`, default `False`) - controls what the mocked
  `search_playlist()` (Spotify's own "is this song really in the playlist you're reporting as
  context" check) answers. Almost every test leaves this at the default, since most scenarios don't
  care what Spotify's search says. Set it `True` to simulate Spotify genuinely confirming a song is
  in whatever playlist it's reporting as context - see "A song on a monitored playlist still counts
  even when Spotify reports a different playlist as context" below for why that distinction matters.
- **`PlaylistSession`'s `playlist_config` argument** accepts either one playlist config dict (most
  tests - the session then tracks it via `session.playlist_name`) or a list of them, for the rare
  scenario that genuinely needs two monitored playlists interacting at once - see "A playlist can
  cross its own threshold while a second monitored playlist is still counting up" below.
- **`build_sequence(specs, step_seconds=180)`** builds a whole list of `song()` entries, 3 minutes
  apart by default, anchored at real "now" moving forward (a past anchor would make every song look
  stale against the barely-advancing mocked clock and the friend would never appear active).
- **`absent()`** - a poll where the friend isn't in the friends list at all (used for the
  "friend disappears" tests, which are a *different* scenario from "friend goes idle" - see the
  two "state survives a gap" sections below for why they're tested separately).
- **`FakeClock`** / **`(entry, clock_value)` tuples** - for the "friend goes idle" tests, a plain
  time-based sequence isn't enough: the friend must appear to still be *present* (same track, same
  friends-list entry) while real elapsed time crosses the inactivity threshold. Each sequence item
  can be `(entry, clock_value)` instead of just `entry`; the harness sets the mocked `time.time()`
  to `clock_value` right before serving that entry, so "how much time has passed" checks are exact
  and reproducible regardless of how fast the test actually executes.
- **`session.output`** vs. **`session.log_output`** - this is the single most important gotcha in
  this harness, and it's worth understanding before adding a new assertion. `ALT_VIEW` mode makes
  the code under test reassign `sys.stdout` to a **file-only** `Logger` right before the main
  polling loop starts (`spotify_monitor.py`, just before "Primary loop"). From that point on, bare
  `print(...)` calls - e.g. `*** Friend got INACTIVE after listening to music for ...` and
  `*** Friend got ACTIVE after being offline for ...` - land **only in the log file**, never in
  `session.output`. Only `print_to_screen()` / `print_to_both()` calls (the song lines, `Detected`/
  `Cleared`) reach `session.output`, because they write straight to the *original* `Logger`'s
  captured terminal stream, bypassing whatever `sys.stdout` currently points at. If you need to
  assert on an idle/resume message, or anything else printed with a bare `print()` inside the main
  loop, check `session.log_output`, not `session.output`.
- **`FRIEND_ACTIVITY_BACKEND`** - `spotify_monitor.py`'s `CONFIG_BLOCK` sets this to
  `"listening_activity"` by default at import time, which makes `activity_inactivity_check()` use
  `SPOTIFY_LIVE_INACTIVITY_CHECK` (default 180s) instead of `SPOTIFY_INACTIVITY_CHECK`. Our mocked
  friend data has no `sp_is_playing` field, i.e. it has the shape of the *other* backend
  (`"buddylist"`). `PlaylistSession` explicitly sets `FRIEND_ACTIVITY_BACKEND = "buddylist"` so that
  its `inactivity_check_seconds` parameter (which patches `SPOTIFY_INACTIVITY_CHECK`) actually takes
  effect. Forgetting this makes any inactivity-threshold test pass **vacuously** - the idle/resume
  code paths silently never run, no matter what the clock values say, because the check compares
  against the wrong (much larger) threshold.
- **`session.song_records()`** parses every "now playing" console line into
  `{offset, track, playlist, icon_add}` - `offset` is **minutes elapsed since the session started**
  (`time_diff_str()`), not seconds. A `build_sequence(..., step_seconds=180)` sequence therefore
  lands song index N at `[N*3]`.
- **`session.detected_offsets()` / `session.cleared_offsets()`** - the `[NN]`-prefixed offsets of
  every `*** Playlist 'X' Detected` / `*** Playlist 'X' Cleared` line.
- A friend "session" (in the `time_diff_str()`/offset sense) restarts every time the friend
  transitions from inactive back to active - see "Friend goes idle, then becomes active again"
  below for why that resets the `[NN]` counter to 0 partway through a test.

## Config helper: `make_playlist(...)`

```python
def make_playlist(name="Test Playlist", qty_start=3, qty_end=2, icon="<3", notify=True,
                   override=False, tracks=("SONGA", "SONGB")):
    return {
        "name": name, "filename": "", "qty_start": qty_start, "qty_end": qty_end,
        "url": "http://playlist", "icon": icon, "notify": notify, "override": override,
        "refresh": 0, "tracks_set": {f"ARTIST - {t}" for t in tracks},
        "count_start": 0, "count_end": 0, "count_shuffle": 0,
    }
```

`qty_start=3, qty_end=2` mirror the real Discovery Zone config's own defaults, so test output reads
the same way real logs do. **`tracks_set` must be `"ARTIST - <TRACK>"`, not a bare track name** -
`find_song_in_playlists()` matches `f"{sp_artist} - {sp_track}".upper()` against it, and all our
synthetic songs use artist `"Artist"`. Getting this wrong was a real bug caught during this suite's
own development: a bare `{"SONGA"}` tracks_set simply never matches anything, and every test built
on it passes "successfully" while testing nothing.

## Assertion helpers

- **`assert_tagged_exactly(session, expected_offsets)`** - every song at one of `expected_offsets`
  must show the `[Playlist Name]` tag; every other song must not. Fails loudly with the offset,
  track, and actual tag if any song's tag state doesn't match - this is what catches "tag leaked
  onto a song that shouldn't have it" or "tag missing from a song that should have it" bugs.
- **`assert_icon_add_exactly(session, expected_offsets)`** - same shape, for the generic `*`
  shuffle-tolerance icon (`ICON_SONG_MISSING_FROM_PLAYLIST`).
- **`assert_events_exactly(session, detected_at=(), cleared_at=())`** - the *exact* list of offsets
  where `Detected`/`Cleared` fired, in order. Exact equality (not "contains") on purpose: an extra,
  unexpected `Detected`/`Cleared` anywhere is exactly the kind of bug this suite exists to catch.

---

## A single on-list song, by itself, must not announce anything

**Test:** `test_first_song_on_playlist_does_not_announce`

**What this verifies:** if the very first song observed happens to be on a monitored playlist, the
tool does *not* immediately treat that as "the friend is listening to this playlist." It only
announces once `qty_start` songs in a row have been seen.

**Why it matters:** without this rule, a coincidental single match (e.g. the friend's Liked Songs
happens to include a song they're playing from an unrelated context) would fire a false "Detected"
after just one song. Requiring several in a row is what makes the feature trustworthy - one song
proves nothing, three in a row is a real pattern.

```python
seq = build_sequence(["SONGA"])           # a single on-list song, [00]
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=3)
assert_tagged_exactly(session, expected_offsets=set())    # no tag
assert_icon_add_exactly(session, expected_offsets=set())  # no icon
assert_events_exactly(session, detected_at=(), cleared_at=())  # no events
```

`qty_start=3` means a playlist needs 3 consecutive on-list songs before it's "Detected". One song
is `count_start == 1`, nowhere near the threshold - `PlaylistTracker.advance()` returns `"none"`,
so nothing is tagged and no notification fires.

---

## The full lifecycle: counting up to detection, tolerating one off-list song, then clearing

**Test:** `test_full_detect_shuffle_clear_cycle`

**What this verifies:** this is the end-to-end "happy path" the whole feature exists for, checked
in one continuous run: a playlist starts uncounted, accumulates a streak, gets **Detected**, stays
tagged while the friend keeps playing from it, survives one off-list "smart shuffle" song without
losing its detected status, and then genuinely **Clears** once a second off-list song confirms the
friend has moved on - after which it goes back to being untracked, exactly like before detection.

**Why it matters:** each of the other tests in this suite isolates one narrow rule; this one proves
those rules actually compose into the intended real-world behavior when run back-to-back, in order,
against the real polling loop - not just as separate unit checks.

```python
seq = build_sequence([
    "OFFLIST1",   # [00] not on playlist - count stays at 0
    "SONGA",      # [03] 1/3
    "SONGB",      # [06] 2/3
    "SONGA",      # [09] 3/3 -> Detected
    "SONGB",      # [12] still in playlist (confirmed - tagged)
    "SONGA",      # [15] still in playlist (confirmed - tagged)
    "OFFLIST2",   # [18] 1st miss (qty_end=2) -> tolerated: shows tag AND the shuffle icon
    "OFFLIST3",   # [21] 2nd miss -> Cleared
    "OFFLIST4",   # [24] no longer tracked - Cleared already fired, plain song line
    "OFFLIST5",   # [27] no longer tracked
])
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=12)
assert_tagged_exactly(session, expected_offsets={9, 12, 15, 18})
assert_icon_add_exactly(session, expected_offsets={18})
assert_events_exactly(session, detected_at=(9,), cleared_at=(21,))
```

**Console shape this produces** (paraphrased from the harness's own regexes; real output has
timestamps too):

```
[00] OFFLIST1 - Artist (Album)
[03] SONGA - Artist (Album)
[06] SONGB - Artist (Album)
*** Playlist 'Test Playlist' Detected
[09] SONGA<3 - Artist (Album) [Test Playlist]
[12] SONGB<3 - Artist (Album) [Test Playlist]
[15] SONGA<3 - Artist (Album) [Test Playlist]
[18] OFFLIST2 - Artist (Album) [Test Playlist]*
*** Playlist 'Test Playlist' Cleared, Song Count: 3
[21] OFFLIST3 - Artist (Album)
[24] OFFLIST4 - Artist (Album)
[27] OFFLIST5 - Artist (Album)
```

**Why each offset is what it is:**
- `[00]` OFFLIST1: not on the list, `count_start` stays 0. Not tagged.
- `[03]`/`[06]`: `count_start` climbs to 1, then 2. Still below `qty_start=3` - not tagged yet
  (this is the same rule the "single on-list song" test above checks in isolation).
- `[09]`: the 3rd consecutive on-list song. `count_start` hits `qty_start` exactly ->
  `advance()` fires the `on_detected` callback and returns `"matched"`. This is the **first**
  song that gets tagged, and the `Detected` message is now expected to print immediately before
  this song's own line (see "message ordering" below).
- `[12]`, `[15]`: still consecutively on-list, `count_start` keeps climbing past `qty_start` -
  stays tagged, no new events (an already-detected playlist doesn't re-announce on every song).
- `[18]`: the first off-list song since detection. `qty_end=2` means up to `qty_end - 1 = 1`
  off-list song in a row is tolerated as a "smart shuffle" exception - `advance()` returns
  `"shuffle"`, `count_shuffle` increments, and the song is tagged with the playlist name (still
  "on" the playlist logically) **plus** the generic `*` icon instead of the playlist's own custom
  icon (see the icon test below for why those two icons are mutually exclusive).
- `[21]`: the second off-list song in a row - `count_end` reaches `qty_end=2`, crossing the
  clearing threshold. `Cleared` fires, and (per the deliberate improvement documented in
  `../test_playlist_detection/README.md`) the "Cleared" line reaches the screen here, not just the
  real notification channels.
- `[24]`, `[27]`: after clearing, `reset_counts()` has zeroed everything - these are back to being
  ordinary, untagged song lines, exactly like `[00]`.

**Message ordering:** `Detected`/`Cleared` print *before* the song line they describe, not after -
e.g. the `*** Playlist 'Test Playlist' Detected` line appears above `[09] SONGA<3 ...`, since the
message describes what just became true as of that song, and reads better leading into it than
trailing it.

---

## A song on a monitored playlist still counts even when Spotify reports a different playlist as context

**Tests:** `test_song_confirmed_in_a_different_reported_playlist_still_counts_toward_a_monitored_one`,
`test_song_confirmed_only_in_a_different_playlist_does_not_count_toward_monitored_one`

**What this verifies:** Spotify reports a "context" playlist for whatever a friend is currently
playing (e.g. a friend's own personal playlist). Separately, `JMK_MODE` asks Spotify to confirm
whether the song genuinely is in that reported playlist (`search_playlist()`). This test verifies
that a **confirmed "yes"** to that question does not, by itself, stop the same song from *also*
being counted toward a monitored playlist (like Discovery Zone) whose own track list happens to
include that song too - two playlists can legitimately share a song, and being confirmed in one
must not disqualify it from the other.

**Why it matters:** this is a real production bug, caught from an actual run: a friend was playing
several songs in a row that were all reported under a personal playlist (something like an
"I Love You!" playlist), and every one of those songs also happened to be on the user's Discovery
Zone track list - yet Discovery Zone was never detected. The cause was Spotify's own confirmation
("yes, this song is in the reported playlist") being treated as the final word, which skipped
checking monitored playlists' track lists entirely. Since a big part of the reason to maintain an
explicit monitored track list in the first place is that Spotify's own reported context can't be
relied on to name every playlist a song matters to, treating Spotify's confirmation as disqualifying
defeated the point of the feature for exactly the songs it most needed to catch.

```python
# Regression case: songs really are confirmed in "My Playlist" (a different, non-monitored
# playlist), but they're ALSO on "Test Playlist"'s own track list - must still detect.
seq = build_sequence([("SONGA", "My Playlist"), ("SONGB", "My Playlist"), ("SONGA", "My Playlist")])
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=6, search_playlist_result=True)
assert_tagged_exactly(session, expected_offsets={6})
assert_events_exactly(session, detected_at=(6,), cleared_at=())

# Control case: songs confirmed in "My Playlist" that are NOT on "Test Playlist"'s track list at
# all must still be left alone - the fix must not loosen matching into "anything Spotify confirms
# anywhere counts everywhere."
seq = build_sequence([("OFFLIST1", "My Playlist"), ("OFFLIST2", "My Playlist"), ("OFFLIST3", "My Playlist")])
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=6, search_playlist_result=True)
assert_tagged_exactly(session, expected_offsets=set())
assert_events_exactly(session, detected_at=(), cleared_at=())
```

`PlaylistSession`'s `search_playlist_result` parameter (default `False`, matching every other test
in this suite) lets these two tests simulate Spotify's `search_playlist()` API call answering `True`
- something no other test needs, since every other scenario relies on the normal "Spotify doesn't
know or care about our monitored playlist" case.

**The fix:** `is_song_in_any_monitored_playlist()` (`spotify_monitor.py`) is checked alongside the
existing `is_playlist_already_monitored_by_name()` wherever `hasTrack` gets computed - if the song
is found on *any* monitored playlist's track list, `hasTrack` is downgraded back to `False` so the
normal monitored-playlist matching (`find_song_in_playlists()` / `PlaylistTracker.advance()`) still
runs, exactly as if Spotify hadn't reported an unrelated context at all. This exact gap existed
in the pre-refactor original code too (verified against `C:\Python Dev\spotify_monitor`) - it isn't
a refactor regression, just a real-world overlap the original algorithm never accounted for.

---

## A Spotify-confirmed different playlist costs one ordinary miss, not an instant clear

**Test:** `test_cleared_via_has_track_resets_counts_and_requires_a_fresh_detection`

**What this verifies:** when Spotify's own search confirms the current song genuinely belongs to a
different, unrelated playlist (a `hasTrack=True` song - see `compute_has_track()`), that song costs
whatever playlist was being tracked exactly **one ordinary miss toward `qty_end`** - the same
tolerance an unconfirmed off-list song gets - rather than instantly clearing it. Only once `qty_end`
such songs land in a row does it actually clear, and at that point its counters must be **fully
reset**, not left with stale progress: a monitored playlist that gets re-matched afterward must go
through a full, fresh `qty_start`-song count-up and get its own new `Detected` announcement, not
instantly reappear as already "matched" from leftover counts.

**Why it matters (two bugs, one branch, fixed at different times):**
- *Reset-on-clear:* real production bug, caught from an actual run - the pre-refactor original code
  even has a comment from the original author marking it as a known, never-fixed issue:
  `# DZ cleared is lost here - 2/28/2026 try to fix #jmk`. The `has_track` branch used to call
  `reset_counts(self.previous['name'])` right after deciding to clear `self.previous` -
  `reset_counts()`'s `protect_name` argument is meant to shield a playlist that's *continuing* to be
  tracked from a reset happening around it, but here it was protecting the exact playlist that had
  just been cleared, so its `count_start` was never actually zeroed. The playlist would silently
  reappear as "matched" (tagged, iconed) a few songs later without a real count-up, and never
  `Detected` again, since `count_start` had already sailed past `qty_start` unnoticed.
- *Instant clear instead of a tolerated miss:* a deliberate design change, made by request after the
  reset bug above was fixed - a friend's music genuinely being confirmed elsewhere for one song
  (e.g. a smart-shuffle insert Spotify happens to also recognize) shouldn't cost a playlist its
  detected status outright when an *unconfirmed* off-list song in the same spot would have been
  tolerated. Making `has_track=True` fall through into the exact same miss-counting logic as an
  ordinary off-list song (rather than its own separate immediate-clear-and-reset path) makes the two
  cases behave identically, as they should.

```python
seq = build_sequence(["SONGA", "SONGB", "SONGA", "OFFLIST1", "OFFLIST2", "SONGA", "SONGB", "SONGA"])
# search_playlist_result=True: OFFLIST1/OFFLIST2 (not on Test Playlist's own list) get
# hasTrack=True, genuinely confirmed elsewhere - the trigger for the has_track miss-counting path.
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=16, search_playlist_result=True)
# Detected twice - once for the first SONGA/SONGB/SONGA run, and again for the one after clearing -
# proving a fresh 3-song count-up was required the second time, not an instant match. Cleared only
# after the SECOND has_track song (qty_end=2): the first one alone must be tolerated.
assert_events_exactly(session, detected_at=(6, 21), cleared_at=(12,))
assert monitor.monitored_playlists_data["Test Playlist"]["count_start"] == 3
```

Reverting the has_track branch to its old "instant clear" form and rerunning this test confirms it
catches a regression back to that behavior precisely: `Cleared` fires one song too early (`[9]`
instead of `[12]`) - the first `has_track` song alone would incorrectly clear the playlist instead of
just being tolerated as one miss.

**The fix:** the `has_track` branch no longer builds its own "cleared" message or calls
`reset_counts()` directly at all - it just sets `self.current = None` (since `has_track=True` already
means the song doesn't match any monitored playlist's own track list, per `compute_has_track()`'s own
downgrade logic) and falls through into the same "playlist not (newly) matched" logic every ordinary
off-list song already goes through, which increments `self.previous['count_end']`, only clears once
that reaches `qty_end`, and - now, since it's the exact same code path as an ordinary clear - resets
counts correctly (`self.reset_counts()` with no `protect_name`) when it does. The old reset-on-clear
bug is fixed as a side effect of reusing this path, rather than needing its own separate fix. Verified
against the pre-refactor original code: it has the same reset bug (down to the same
`found_playlist`/`last_found_playlist` aliasing that causes it), but not the miss-counting question -
the design change described above is new behavior, not a restoration of prior behavior.

---

## A Cleared/Detected message triggered by the very song that resumes a session must print after the "Start notification sent" banner, not before it

**Test:** `test_resumed_session_clear_prints_after_start_notification`

**What this verifies:** when the very first song observed after a friend resumes from being idle
also triggers a real `Cleared` (or `Detected`) through the *normal* per-song `tracker.advance()`
call - not the separate "already-detected, re-announce" recheck a bit further down - that message
must print **after** the new session's own `"*** Start notification sent"` banner, not before it, as
if it belonged to the session that just ended.

**Why it matters:** this is a real production bug, caught from an actual run - a `Cleared` line
appeared *before* `"*** Start notification sent"` for the friend's new session, reading as if the
just-ended session's playlist had cleared after the fact, when it was really the brand new song that
triggered it. The root cause: the normal `tracker.advance()` call always runs structurally *before*
the "friend resumed" block that prints the banner, and `advance()` has to print its own
detected/cleared line eagerly in several branches (because a later `reset_counts()` call within that
same `advance()` invocation would otherwise wipe the message before anyone saw it) - so, without
special handling, that eager print always lands before the banner whenever both happen to fire for
the same song.

```python
base = int(real_time.time())
seq = [
    (song("SONGA", 0, "Today's Top Hits", ..., base), base),
    (song("SONGB", 180, "Today's Top Hits", ..., base), base + 180),
    (song("SONGA", 360, "Today's Top Hits", ..., base), base + 360),  # 3/3 -> Detected
    (song("SONGA", 360, "Today's Top Hits", ..., base), base + 450),  # idle detected here
    # Resumes on a song Spotify confirms belongs to a different, unrelated playlist - this triggers
    # the has_track miss-counting path on the very same song that starts the new session, and (with
    # qty_end=1 below) crosses the threshold on that first miss.
    (song("OFFLIST1", 600, "Some Other Playlist", ..., base), base + 610),
]
session = PlaylistSession(monkeypatch, make_playlist(qty_end=1), seq, iterations=20, inactivity_check_seconds=60,
                           search_playlist_result=True)
assert "got ACTIVE after being offline" in session.log_output   # the resume itself must actually fire
start_idx = session.output.rindex("Start notification sent")
cleared_idx = session.output.rindex("Cleared")
assert start_idx < cleared_idx
```

`qty_end=1` (instead of the usual default of 2) makes the single off-list song that resumes the
session enough, by itself, to cross the miss threshold and fire `Cleared` right then - putting the
ordering question to the test on the very first song of a brand new session, which is exactly the
situation that originally exposed the bug.

Reverting the fix and rerunning this test confirms it catches the bug precisely: `cleared_idx` comes
back *before* `start_idx`, i.e. the assertion fails with `Cleared` printing ahead of `Start
notification sent`, matching the reported symptom.

**The fix:** `PlaylistTracker.advance()` gained a `defer_screen_message` parameter and a
`self.pending_screen_message` slot (via a small `_emit_screen_message()` helper). The two "Cleared"
call sites honor it: instead of printing immediately, they stash the message for the caller to show
itself once it's actually ready to. The LOOP C call site passes `defer_screen_message=` a
`friend_resuming_this_song` flag (true exactly when this call's song is the one that resumes the
friend from idle); the "friend resumed" block then flushes `tracker.pending_screen_message` right
after printing `"Start notification sent"`, so the order always comes out correct. The "Detected"
sites are deliberately **not** deferred - see the next section for why that's a fine tradeoff, not an
oversight.

---

## The "already announced" guard was dropped in favor of deferring only where it's actually needed

**No dedicated test** - this was a same-session simplification of the fix above, not a new bug.

The `defer_screen_message` mechanism above originally shipped with a broad guard: after flushing
`tracker.pending_screen_message`, the "friend resumed" block's own "already-detected, re-announce"
recheck was skipped entirely whenever *anything* had been deferred, to avoid announcing the same
playlist twice. That guard was broader than it needed to be - of `advance()`'s three
detected/cleared call sites, only the two "Cleared" ones can produce a message the recheck could
plausibly duplicate; the recheck itself only ever rebuilds a "Detected" message, so a deferred
"Cleared" can never collide with it, and neither can an already-immediately-printed "Detected".

The simplification: the exception-branch "Detected" site now always emits immediately, ignoring
`defer_screen_message` (see the comment there for a narrow accepted tradeoff: on the rare resumed
song that hits that exact branch, its message can still print before the "Start notification sent"
banner - a much narrower case than the one the test above guards, and one that would need its own
double-announce guard against the recheck to fix). With that in place, `tracker.pending_screen_message`
can only ever hold a "Cleared" message, so the recheck can simply run unconditionally after flushing
it, with no guard variable needed at all.

---

## A friend's stale last-known song must not be counted twice when they resume

**Test:** `test_stale_boot_song_is_not_double_counted_on_resume`

**What this verifies:** when a friend shows offline/stale right when the monitor (re)acquires them,
whatever they were last playing is history, not something happening right now - it must not be
counted toward a monitored playlist's progress. If that friend then resumes and Spotify reports
that *same* track again (with a fresh activity timestamp, since a genuinely new play just started),
it must be counted exactly **once** - not once at boot and once again on resume.

**Why it matters:** this is a real production bug, caught from an actual run. The friend showed as
offline at boot with `Here Tonight` as their last-known song, which also happened to be genuinely on
Discovery Zone Test's track list. The boot-time snapshot counted it once; moments later, the friend
resumed on that exact same track, and it got counted a second time - `Discovery Zone Test` was
Detected after only 2 *new* songs that session, when `qty_start=3` should have required 3. The root
cause: the boot-time snapshot ran unconditionally, whether or not the friend actually looked active,
and the resume check (`track_changed`) compares only Spotify's reported activity *timestamp*, not
track identity - so a same-track-but-newer-timestamp sample reads as a brand new song and gets
recounted.

```python
base = int(real_time.time())
seq = [
    # Boot sample: SONGA's own reported timestamp is old (offset 0), but the mocked clock is
    # already far ahead (+700s) when this is served, so cur_ts - sp_ts (700s) exceeds the 60s
    # inactivity threshold - the friend must appear offline/stale at boot, not active.
    (song("SONGA", 0, "Today's Top Hits", ..., base), base + 700),
    # Friend resumes on the SAME track - a fresh reported timestamp (offset 700) for a track
    # that's identical to the stale boot sample.
    (song("SONGA", 700, "Today's Top Hits", ..., base), base + 700),
    (song("SONGB", 880, "Today's Top Hits", ..., base), base + 880),
    (song("SONGC", 1060, "Today's Top Hits", ..., base), base + 1060),
]
session = PlaylistSession(monkeypatch, make_playlist(tracks=("SONGA", "SONGB", "SONGC")), seq,
                           iterations=20, inactivity_check_seconds=60)
playlist = monitor.monitored_playlists_data[session.playlist_name]
# Exactly 3 distinct on-list songs (resumed SONGA, SONGB, SONGC) - not 4 (SONGA counted twice).
assert playlist["count_start"] == 3
# Detected must land on SONGC (the 3rd distinct song), not SONGB.
songc_offset = next(r["offset"] for r in session.song_records() if r["track"].startswith("SONGC"))
assert_events_exactly(session, detected_at=(songc_offset,), cleared_at=())
```

Reverting the fix and rerunning this test confirms it actually catches the bug: `count_start` comes
back as `4` instead of `3` (SONGA counted at boot *and* again on resume), and `Detected` fires one
song too early (at SONGB instead of SONGC) - matching the exact real-world log pattern this test was
built from.

**The fix:** the boot-time snapshot (`spotify_monitor.py`'s "LOOP A - FIRST BOOT UP" pass) now only
runs `tracker.advance()` - the call that actually counts a song toward a monitored playlist - when
`initially_active` is `True` (the friend genuinely appears active right now, not just showing a
last-known song from however long ago). `initially_active` itself was moved earlier in that function
so it could gate this call; when the friend is offline/stale at boot, `outcome` is set to `"none"`
directly and the snapshot's own counting is skipped entirely, leaving the real count to happen once,
for real, when `LOOP C` observes the resumed track as a genuine "track changed" event. Verified
identical in the pre-refactor original code too - not a refactor regression.

---

## A playlist can cross its own threshold while a second monitored playlist is still counting up

**Test:** `test_playlist_detected_via_exception_branch_while_a_second_playlist_still_counting_up`

**What this verifies:** with two monitored playlists configured, one playlist's progress can cross
its own `qty_start` threshold at a moment when `PlaylistTracker` is technically tracking a
*different* playlist as an "exception" (a song matches playlist A by name/track-list while playlist
B - the one being tracked - hasn't used up its own miss tolerance yet, so it's treated as a
tolerated exception rather than a hard switch away from B). This must still announce `Detected` for
A at the exact song that crossed the threshold - not silently, and not one song later.

**Why it matters:** this is a real production bug, caught from an actual run with two active
playlists (`Discovery Zone Test` and `Liked Songs Test`). A song matched `Discovery Zone Test` by
name while `Liked Songs Test` was still being tracked and hadn't exhausted its own tolerance - this
routed through the "exception" branch, which incremented `Discovery Zone Test`'s count *without
ever checking whether that increment crossed its own threshold*. The count silently reached
`qty_start`, and by the time the *next* song naturally re-matched `Discovery Zone Test`, its count
was already past threshold (`count_start != qty_start`), so the exact-equality check that builds the
"Detected" message never fired there either. The playlist just quietly became tagged and iconed as
if it had always been detected, with no `Detected` announcement ever appearing anywhere - exactly
what was reported.

```python
# qty_end is generous on both so neither playlist clears mid-test.
playlist_a = make_playlist(name="Test Playlist", qty_start=3, qty_end=5, tracks=("SONGX", "SONGX2", "SONGX3", "SONGX4"))
playlist_b = make_playlist(name="Other Playlist", qty_start=3, qty_end=5, tracks=("SONGY",))
seq = build_sequence([
    ("SONGX", "Some Context"),   # Test Playlist: count_start 0 -> 1
    ("SONGX2", "Some Context"),  # Test Playlist: count_start 1 -> 2
    ("SONGY", "Some Context"),   # Other Playlist becomes current (Test Playlist still tolerating misses)
    ("SONGX3", "Some Context"),  # Test Playlist is current again, as an EXCEPTION to Other Playlist
                                  # (which hasn't hit its own qty_start) - count_start 2 -> 3 = qty_start
    ("SONGX4", "Some Context"),  # an ordinary continuation, now clearly past threshold
])
session = PlaylistSession(monkeypatch, [playlist_a, playlist_b], seq, iterations=8)
songx3_offset = next(r["offset"] for r in session.song_records() if r["track"].startswith("SONGX3"))
assert_events_exactly(session, detected_at=(songx3_offset,), cleared_at=())
assert monitor.monitored_playlists_data["Test Playlist"]["count_start"] == 4
```

Reverting the fix and rerunning this test confirms it actually catches the bug: `Detected` doesn't
fire at all anywhere in the sequence (`detected_offsets()` comes back empty) - matching the reported
symptom exactly, rather than merely firing at the wrong offset.

**The fix:** `PlaylistTracker.advance()`'s "playlist not (newly) matched, or an exception to the one
we were already tracking" branch now runs the same "did this increment just cross `qty_start`" check
the main matching branch already had, immediately after incrementing the exception playlist's
`count_start` - building and (eagerly, for `ALT_VIEW`) printing the `Detected` message right then,
via the same `on_detected()` callback the main branch uses, rather than only ever checking that
condition in the one branch this scenario never reaches. Verified identical in the pre-refactor
original code too - not a refactor regression.

---

## The playlist's own icon and the generic "off-list" icon never appear on the same song

**Test:** `test_custom_icon_shown_on_matched_songs_not_on_shuffle_songs`
(parametrized over `icon=" <3"` and `icon=" ♥"` i.e. `" ♥"`, to prove multi-byte/Unicode icons
work identically to plain-ASCII ones)

**What this verifies:** there are two visually different icons in play, and they mean two different
things: the playlist's configured icon (e.g. `<3`) means "this song is genuinely on the list", and
the generic `*` means "this song isn't on the list, but we're tolerating it as a shuffle exception."
This test confirms they're never confused - a confirmed song never shows `*`, and a tolerated
off-list song never shows the playlist's custom icon.

**Why it matters:** a prior refactor of this code introduced a real bug where the generic `*` icon,
once shown, never went away again - every subsequent song kept showing it, confirmed match or not
(see `../test_playlist_detection/README.md`, regression #2). This test is the guard against that
regression coming back, and against the inverse mistake (custom icon leaking onto a shuffle song).

```python
seq = build_sequence(["SONGA", "SONGB", "SONGA", "OFFLIST1"])  # offsets: 0, 3, 6, 9
session = PlaylistSession(monkeypatch, make_playlist(icon=icon), seq, iterations=6)
records = {r["offset"]: r for r in session.song_records()}
assert records[6]["track"] == f"SONGA{icon}"      # e.g. "SONGA <3" or "SONGA ♥"
assert records[9]["track"] == "OFFLIST1"          # custom icon NOT appended here
assert records[9]["icon_add"] is True             # generic "*" IS shown here instead
assert_events_exactly(session, detected_at=(6,), cleared_at=())
```

- The playlist's own **custom icon** (`icon` config field, e.g. `" <3"` or `" ♥"`) is appended
  directly onto the track name (`sp_track = sp_track + icon`) whenever a song is a **confirmed
  match** on the playlist (`[06]` - the 3rd consecutive `SONGA`, the moment of detection).
- The **generic `*`** (`ICON_SONG_MISSING_FROM_PLAYLIST`) is a separate flag (`icon_add`, tracked
  by the caller's `icon_add`/`clear_icon_add()` closure, driven by `PlaylistTracker`'s `on_reset`
  callback) shown next to the `[Playlist Name]` tag whenever the *current* song is a tolerated
  off-list exception (`"shuffle"` outcome) - `[09]` here. It marks "this song itself isn't really
  on the list, but we're still counting the playlist as active."
- `records[9]["icon_add"] is True` alone wouldn't have caught the old regression; it's the
  combination with checking `[06]` (and every song around it) that proves the icon actually turns
  off again rather than sticking.

---

## Friend goes idle, then becomes active again - playlist state must survive

This is the scenario that took the most work to get right, so it's documented in the most detail.
**"Idle" here specifically means the friend's Spotify *activity* goes inactive and later becomes
active again while the friend never disappears from the friends list** - the kind of gap you'd see
if a friend closes Spotify, or their phone locks, for several minutes and then starts playing music
again. This is a *different* real-world situation from the friend literally vanishing from the
friends-list API response (see "Friend disappears from the friends list" below), and the code
handles them via two different mechanisms, so they're tested separately:
- **Idle (this section):** the "track NOT changed" branch of the main polling loop notices real time
  has passed the inactivity threshold since the last confirmed activity, prints
  `*** Friend got INACTIVE after listening to music for ...`, and later, once a *new* track is
  finally observed, prints `*** Friend got ACTIVE after being offline for ...` and starts a fresh
  "session" (the `[NN]` offset counter in `time_diff_str()` resets to 0).
- **Disappeared (the section after this one):** the friend is simply missing from the friends-list
  JSON for a while (e.g. activity sharing temporarily off, or a transient API hiccup) - a completely
  different code path (`disappeared_counter` / "has disappeared" / "has reappeared"), which does
  **not** reset the session or its offset counter the same way.

**What both tests below verify:** that the playlist's tag, its detected/not-detected status, and
its underlying counters (`count_start`, `count_end`, `count_shuffle`) all survive this idle gap
intact - the friend going quiet for a while must never look like the friend leaving the playlist,
and must never silently reset progress that had already accumulated.

**Why it matters:** this was the specific real-world case the user asked to have verified - a
friend who steps away and comes back should not have to "re-earn" a playlist detection that was
already correct, and the tool should not falsely announce a clear just because nothing happened for
a few minutes.

### Resuming with another on-list song

**Test:** `test_state_survives_going_idle_then_active_with_on_list_song`

```python
base = int(real_time.time())
seq = [
    (song("SONGA", 0,   "Today's Top Hits", ..., base), base),
    (song("SONGB", 180, "Today's Top Hits", ..., base), base + 180),
    (song("SONGA", 360, "Today's Top Hits", ..., base), base + 360),   # 3/3 -> Detected
    # friend goes idle: the SAME track (SONGA) repeats while the mocked clock keeps advancing
    # past the 60s inactivity threshold, without a single new song being observed
    (song("SONGA", 360, "Today's Top Hits", ..., base), base + 380),
    (song("SONGA", 360, "Today's Top Hits", ..., base), base + 450),   # idle detected here
    # friend becomes active again with a new on-list song
    (song("SONGB", 600, "Today's Top Hits", ..., base), base + 610),
    (song("SONGA", 780, "Today's Top Hits", ..., base), base + 790),
]
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=20, inactivity_check_seconds=60)
```

Each tuple is `(friends_list_entry, clock_value)` - the entry's own reported timestamp stays fixed
at `offset=360` for the three "idle" entries (so `track_changed` correctly evaluates `False`, since
Spotify itself is reporting the same unchanged `sp_ts`), while the *mocked wall clock* advances
underneath it (`+360`, `+380`, `+450`) to simulate real time passing with nothing new happening.
`450 - 360 = 90 > inactivity_check_seconds (60)` is what actually crosses the threshold.

**What's asserted, and why each assertion exists:**

1. **`"got INACTIVE" in session.log_output`** and **`"got ACTIVE after being offline" in
   session.log_output`** - proves the transition *actually fired*, not just that the test didn't
   crash. Note `session.log_output`, not `session.output` - see "How the harness works" above for
   why these particular messages only ever reach the log file. Without this check, the two
   surrounding assertions (tag/count survival) would pass **vacuously** if the idle/resume
   mechanism silently never triggered - which is exactly what happened during this suite's own
   development (wrong `FRIEND_ACTIVITY_BACKEND`, see "How the harness works") and went unnoticed
   until this explicit check was added.
2. **`assert_events_exactly(session, detected_at=(6, 0), cleared_at=())`** - `Detected` fires
   twice: once normally at `[06]` (3rd consecutive `SONGA`), and again at the *new* session's
   `[00]`. That second one is not a bug - a fresh "session" boot (the friend becoming active again)
   re-announces `Detected` for a playlist that already met the threshold before the gap, which
   matches the **original, pre-refactor code's own explicit design** (its own comment reads:
   *"this is needed to cause detection messaging/notifications when user becomes active and
   already on a detected playlist"*). If you see this and think "that's a duplicate, my change
   broke something" - check the original behavior first; it's supposed to happen.
3. `records[0]` and `records[3]` (the post-resume `SONGB` and `SONGA`, renumbered from what would
   have been `[10]`/`[13]` had the session not restarted) must still carry the `[Test Playlist]`
   tag - proving the tag genuinely survived the gap rather than the playlist having been silently
   un-matched.
4. `playlist["count_start"] >= 5` - the counters kept accumulating (3 before the gap, +2 for the
   two post-resume on-list songs), rather than being reset to 0 or 1 by the idle transition.
5. `playlist["count_end"] == 0` and `session.notifications_of_type("cleared") == []` - going idle,
   by itself, must never look like an off-list miss. Nothing here was off the playlist; the friend
   was just quiet.

### Resuming with off-list songs that go on to clear it

**Test:** `test_state_survives_going_idle_then_shuffle_then_clear`

Same idle/resume setup as above, but this time the friend resumes with **off-list** songs, so this
test additionally verifies that the shuffle-tolerance and clearing logic still work correctly
*right after* an idle gap, not just plain tag persistence:

```python
seq = [
    (song("SONGA", 0,   ...), base),
    (song("SONGB", 180, ...), base + 180),
    (song("SONGA", 360, ...), base + 360),   # 3/3 -> Detected
    (song("SONGA", 360, ...), base + 450),   # idle detected here
    (song("OFFLIST1", 600, ...), base + 610),  # resumes off-list: tolerated (qty_end=2)
    (song("OFFLIST2", 780, ...), base + 790),  # 2nd off-list in a row -> Cleared
]
```

- Same `"got INACTIVE"` / `"got ACTIVE after being offline"` proof-of-firing check as above.
- `assert_events_exactly(session, detected_at=(6, 0), cleared_at=(3,))` - `Detected` at `[06]`
  then re-announced at the new session's `[00]` (same reasoning as the previous test); `Cleared`
  at the new session's `[03]` (would have been `[21]` in the original offset numbering, but the
  session restarted at resume, so it's `[03]` - the 2nd song after the new `[00]`).
- `records[0]["playlist"] == session.playlist_name and records[0]["icon_add"] is True` - the first
  off-list song right after resuming is still treated as a tolerated shuffle exception (the
  `count_end`/`count_start` state carried across the gap, so the algorithm correctly picks up
  mid-tolerance rather than starting a fresh "just detected" count).
- `records[3]["playlist"] != session.playlist_name` and `records[3]["icon_add"] is False` - once
  the 2nd off-list song clears it, neither the tag nor the shuffle icon should show (Spotify's own
  "Today's Top Hits" context is what's reported instead for this song, which is correct - it's
  what Spotify itself says, not our tag leaking).

---

## Friend disappears from the friends list, then reappears - playlist state must survive

**What this verifies:** distinct from the idle scenario above - here the friend is simply **absent
from the friends-list API response** for a while (`absent()` polls returning `{"friends": []}`),
the kind of gap you'd see from a transient API hiccup or the friend briefly turning off activity
sharing. No new "session" starts here the way it does after an idle→active transition
(`time_diff_str()`'s offset counter is unaffected) - these two tests only check that state genuinely
survives the disappearance, in both directions (still on the list, and no longer on the list).

**Why it matters:** a flaky API response or a brief visibility toggle is a very different situation
from the friend actually stopping the playlist, and must not be treated the same way - a monitoring
tool that loses track of state every time a poll comes back empty would be far too jumpy to trust.

### Reappearing while still on the playlist

**Test:** `test_state_survives_friend_disappearing_and_reappearing_on_list`

```python
seq = build_sequence(["SONGA", "SONGB", "SONGA"]) + [absent()] * 4 + build_sequence(["SONGB"], step_seconds=180)
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=14)
assert len(session.detected_offsets()) == 1        # only the original Detected, no duplicate
assert records[-1]["playlist"] == session.playlist_name   # tag survives the gap
assert session.cleared_offsets() == []             # a friends-list gap must never look like a clear
```

3 on-list songs detect the playlist; 4 `absent()` polls simulate the friend vanishing from the
friends list; a final on-list song after reappearing must still carry the tag, with no
re-announcement and no false clear.

### Reappearing with off-list songs that go on to clear it

**Test:** `test_state_survives_disappearing_then_clears_on_return`

```python
seq = build_sequence(["SONGA", "SONGB", "SONGA"]) + [absent()] * 4 + build_sequence(["OFFLIST1", "OFFLIST2"], step_seconds=180)
session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=16)
assert len(session.detected_offsets()) == 1
assert len(session.cleared_offsets()) == 1   # two off-list songs after returning should still clear (qty_end=2)
```

Confirms the *opposite* case still works too: after reappearing, two genuinely off-list songs in a
row still clear the playlist normally - the disappearance gap doesn't grant extra tolerance, and
doesn't break the clearing logic either.

---

## `override`: treating the friend as already mid-playlist from the very first sample

**Tests:** `test_override_detects_on_first_sample`, `test_override_false_does_not_jump_start`

**What this verifies:** with `override=True`, a single observed on-list song is enough to
immediately announce **Detected** - it does not need to wait for `qty_start` songs in a row.
With `override=False` (the default), a single song behaves exactly like the "single on-list song"
test earlier: not enough by itself.

**Why it matters:** `override` exists for the case where the friend was *already* partway through
(or fully into) the playlist before monitoring even started - without it, the tool would make you
wait through another full `qty_start`-song streak to notice something that was already true the
moment monitoring began.

```python
seq = build_sequence(["SONGA"])   # a single on-list song, [00]

# override=True
session = PlaylistSession(monkeypatch, make_playlist(override=True), seq, iterations=3)
assert_tagged_exactly(session, expected_offsets={0})
assert_events_exactly(session, detected_at=(0,), cleared_at=())

# override=False (the default)
session = PlaylistSession(monkeypatch, make_playlist(override=False), seq, iterations=3)
assert_tagged_exactly(session, expected_offsets=set())
assert_events_exactly(session, detected_at=(), cleared_at=())
```

Mechanically: the very first match of a session jump-starts `count_start` straight to `qty_start`
(`apply_override`, only ever `True` on a session's first sample - see `PlaylistTracker.advance()`'s
docstring).

---

## `notify`: controls only the real notification, never the on-screen text

**Tests:** `test_notify_false_suppresses_real_notification_but_not_screen_text`,
`test_notify_true_sends_real_notification`

**What this verifies:** the per-playlist `notify` setting only decides whether a *real* outbound
notification (email/push/spreadsheet) gets sent when the playlist is detected. It has no effect on
whether the console/log still shows the tag and the `Detected`/`Cleared` line - those always show,
regardless of `notify`.

**Why it matters:** it would be easy to accidentally wire `notify` up to suppress the on-screen
text too (they're conceptually adjacent), which would make the console misleading - you'd have no
visual confirmation the tool noticed the playlist at all, just because you didn't want an email
about it. These two tests exist specifically to keep those two things decoupled.

```python
seq = build_sequence(["SONGA", "SONGB", "SONGA"])  # offsets: 0, 3, 6 -> Detected at [06]

# notify=False
session = PlaylistSession(monkeypatch, make_playlist(notify=False), seq, iterations=6)
assert_events_exactly(session, detected_at=(6,), cleared_at=())   # screen text still shows it
assert session.notifications_of_type("detected") == []            # but no real notification fires

# notify=True
session = PlaylistSession(monkeypatch, make_playlist(notify=True), seq, iterations=6)
assert_events_exactly(session, detected_at=(6,), cleared_at=())
assert len(session.notifications_of_type("detected")) == 1
```

Worth noting: `PlaylistTracker.advance()` also has its *own*, same-named `notify` *parameter* - but
that one means something different (a session-level "has anything been observed transitioning yet
this session" flag, not the playlist's own config setting). The two are easy to conflate by name
alone; see the docstring on `advance()` for the distinction.

---

## Config validation - catching a bad `ADD_PLAYLISTS_TO_MONITOR` entry before it causes problems

**Test class:** `TestValidateAddPlaylistsToMonitor`

**What this verifies:** `validate_add_playlists_to_monitor()` checks every configured playlist
entry's shape, types, and value ranges *before* any of the detection logic above ever touches it.
A malformed entry is dropped, with a clear error message, instead of being allowed through to fail
in some confusing way deep inside the detection loop later (or silently behaving in a way the
numbers don't actually support, like a threshold that can never be reached).

**Why it matters:** `ADD_PLAYLISTS_TO_MONITOR` is hand-edited config, and hand-edited config
inevitably has typos - a missing quote, a `qty_start` of `0`, a `refresh` accidentally given in the
wrong unit. Without this validation step, a single bad entry could crash the whole monitoring
process, or (worse) silently "work" in a way that never actually detects or clears anything, with
no indication why. Validation trades that failure mode for one clear, specific error message and a
dropped entry - every *other* configured playlist keeps working normally.

Fields it checks:

| Field | Required? | Rule |
|---|---|---|
| `name` | required | non-empty `str`; must also be unique across all entries (it's the dict key into `monitored_playlists_data` - a duplicate would silently overwrite the earlier entry's live counters) |
| `filename` | required | non-empty `str` |
| `qty_start`, `qty_end` | required | `int` (not `bool` - `True`/`False` are technically `int` subclasses in Python but rejected here), and `>= 1` (0 or negative can never be satisfied) |
| `override`, `notify` | optional | `bool` if present |
| `refresh` | optional | `int`/`float`, `>= 0` (0 means "never reload"), and `<= 30 days` (`_MAX_SANE_REFRESH_SECONDS` - anything past that is almost certainly a units typo, e.g. minutes instead of seconds) |
| `url`, `icon` | optional | `str` if present |
| anything else | ignored | logged via `print_debug`, entry still kept - config files can carry forward-compatible/future fields without being rejected |

An autouse fixture (`_silence_error_output`) stubs `print_to_both` to a no-op for this whole class,
since the real one requires a fully set-up `log_logger` that's irrelevant to what these tests check
(the filtered return value, not the printed text).

**Tests:**

- **`test_valid_entry_is_kept`** - a minimal well-formed entry survives validation unchanged. The
  baseline: validation shouldn't reject something that's actually fine.
- **`test_real_world_config_is_kept`** - the *actual* Discovery Zone / Liked Songs config shapes
  (real-looking playlist URL, `"Liked Songs (no URL)"` placeholder URL, `♥` icon, `override=True`)
  both pass through untouched, in their original order. This is the regression guard for "a config
  shape that works in production must never start failing silently after a validator change."
- **`test_invalid_entry_is_dropped`** - parametrized over 16 distinct single-field violations, each
  dropped to `[]` (the whole malformed entry is discarded, not patched/coerced):
  `name=""`, `name=123` (wrong type), `filename=""`, `filename=None`, `qty_start="three"` (wrong
  type), `qty_start=0`, `qty_start=-1`, `qty_end=0`, `qty_end=True` (bool rejected even though
  `isinstance(True, int)` is `True` in Python), `override="yes"` (wrong type), `notify=1` (wrong
  type), `refresh=-5`, `refresh=99_999_999` (>30 days), `refresh="3600"` (wrong type - must be a
  real number, not a numeric string), `url=5`, `icon=5`. Each represents a plausible real-world typo
  someone could actually make while hand-editing a config file.
- **`test_non_dict_entry_is_dropped`** - `["not a dict", 5, None]` all get dropped; a malformed
  `ADD_PLAYLISTS_TO_MONITOR` list (e.g. from a hand-edited config file) can't crash the loop that
  processes it.
- **`test_duplicate_names_second_one_dropped`** - two entries named `"Dup"` -> only the *first* one
  survives, keeping its own `filename`, not the second's - order-sensitive, deliberately, since
  `name` doubles as the tracking key and a duplicate would otherwise silently overwrite live state.
- **`test_one_bad_entry_does_not_affect_others`** - one good entry (`"Good"`) and one bad entry
  (`"Bad"`, `qty_start=0`) in the same list -> only `"Good"` survives. A typo in one playlist's
  config must never take down monitoring of every other playlist.
- **`test_zero_refresh_is_valid`** - `refresh=0` is explicitly valid (means "don't reload"), not an
  error - distinguishing "boundary-valid" from "boundary-invalid" (`qty_start`/`qty_end`'s `0` case,
  by contrast, *is* invalid, since a threshold of 0 can never be meaningfully satisfied).
- **`test_unknown_key_is_tolerated_not_rejected`** - an entry with an unrecognized extra key
  (`some_future_field`) is still kept (just logged via `print_debug`), so config files remain
  forward-compatible with future options this validator doesn't know about yet.
