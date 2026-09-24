# Playlist-detection end-to-end test harness

This directory holds an end-to-end test harness for the monitored-playlist detection feature
(`PlaylistTracker` / `ADD_PLAYLISTS_TO_MONITOR` in `spotify_monitor.py`), used to verify the
[playlist-detection refactor](../README.md) behaves identically to the original code.

**This harness is manual** (compares this codebase against another one you point it at, by
running each and diffing the output) - it's for "did a change alter behavior", not something
`pytest` runs on its own. For automated, assertion-based scenario coverage that runs as part of
the normal test suite (`pytest`), see `../tests/test_playlist_detection_scenarios.py` instead -
it drives the same `spotify_monitor_friend_uri()` loop but with a synthetic monitored playlist and
precise assertions (which songs get tagged, which get the shuffle icon, exactly where Detected/
Cleared fire and nowhere else), covering the full detect → shuffle-tolerance → clear cycle,
custom/Unicode icons, `override`, `notify`, surviving a friends-list gap, and the
`validate_add_playlists_to_monitor()` config-validation checks below.

## Files

- **`test_main_loop.py`** and **`test_fixtures.py`** — the original test harness (unmodified,
  copied in as-is). Written to drive `spotify_monitor.main()` with real Spotify network calls for
  everything except the friends-list poll (which comes from canned `test_fixtures.py` sequences),
  `time.sleep`, and the inactivity clock. Meant to be run interactively, with real credentials, to
  manually watch the monitor react to a scripted sequence of "friend is listening to X" events
  (press Ctrl+C to stop). See the docstring in `test_main_loop.py` for the exact mocking it does.

  To run this one for real (needs a working `.env`/`.conf` one directory up, i.e. in the repo
  root):
  ```
  cd test_playlist_detection
  PYTHONPATH=.. python test_main_loop.py
  ```
  Edit `FRIENDS_SEQUENCE` at the top of `test_main_loop.py` to pick which `SEQUENCE_*` from
  `test_fixtures.py` to play back.

- **`run_against_target.py`** — a non-interactive variant of the same idea, written for this
  refactor. It calls `spotify_monitor_friend_uri()` directly (bypassing `main()`'s CLI/config
  startup) for a **bounded** number of iterations against **any** `spotify_monitor.py` directory
  you point it at, and additionally stubs out everything `test_main_loop.py` itself doesn't mock:
  the Spotify auth token, track/playlist metadata, the `JMK_MODE` `hasTrack` search, and every
  outbound notification (email/push/spreadsheet) - captured instead of sent. It also seeds one
  synthetic monitored playlist, `"Test Playlist"` (containing "Umbrella" and "Love On The Brain"
  by Rihanna - both already appear in every fixture sequence), with `qty_start=3, qty_end=2` -
  matching the real Discovery Zone config's defaults, so the counts here read the same way your
  real logs do - so there's something real for the detection/clearing logic to match against
  without needing your actual `dz_songs.txt`.

  ```
  python run_against_target.py <spotify_monitor.py directory> <SEQUENCE_NAME> <iterations> [output_file]
  # e.g.
  python run_against_target.py .. SEQUENCE_DISCOVERY_ZONE_DETECT 20
  ```

  `SEQUENCE_NAME` can be any `SEQUENCE_*` from `test_fixtures.py`, or `SEQUENCE_DETECT_THEN_CLEAR`
  from `demo_fixtures.py` (see below) - none of the original 5 sequences happen to complete a full
  detect-then-clear cycle, since they all end by repeating their last song forever, which freezes
  `track_changed` before a clear could occur.

- **`demo_fixtures.py`** — one additional sequence, `SEQUENCE_DETECT_THEN_CLEAR`, in the same
  shape as `test_fixtures.py`'s own, built specifically to demonstrate a full
  Detected → (tolerated miss) → Cleared cycle against the real `spotify_monitor_friend_uri()` loop.
  Not part of the original harness - added here because none of `test_fixtures.py`'s own sequences
  exercise that cycle.

- **`compare_with_original.py`** — runs every `SEQUENCE_*` in `test_fixtures.py` through
  `run_against_target.py` against **this repo** and against a comparison codebase (defaults to
  `C:\Python Dev\spotify_monitor`, override with a command-line argument), and diffs the resulting
  notification text (with timestamps normalized out, since two separate process runs a moment
  apart never share a clock tick). This is the actual regression check.

  ```
  python compare_with_original.py
  python compare_with_original.py "C:\path\to\other\spotify_monitor"
  ```

## Why this exists

The project's own `pytest` suite (in `../tests/`) doesn't exercise the monitored-playlist feature
at all - it's a custom addition on top of the upstream project, not something the upstream tests
know about. Static review and a hand-written synthetic-scenario script (exercising
`PlaylistTracker.advance()` directly, not shown here) both gave real signal during the refactor,
but neither one runs the *actual* code end-to-end the way a real monitoring session would. This
harness does: it drives the real `spotify_monitor_friend_uri()` loop, through the real
notification-formatting functions, against the same fixture data the original author already
had, so "does this refactor change observable behavior" has a concrete, repeatable answer instead
of a code-review guess.

## What it found

Running all 5 fixture sequences against the refactored code and the original side by side (via
`compare_with_original.py`) surfaced two real regressions the refactor had introduced, neither of
which the pytest suite or the synthetic scenario check had caught:

1. **Wrong playlist name in the "Detected" notification's embedded "now playing" text.** The
   refactor evaluated that text (`songstring()`/`sp_track`, which read caller-owned display
   state) *before* calling `PlaylistTracker.advance()`, while the original applies the same
   display update inline, *before* building that one specific notification. Fixed by adding an
   `on_detected` callback that `advance()` invokes at the exact right moment, letting the caller
   update its display state first and hand back a freshly-built `songstr`/`sp_track` for the
   notification.

2. **A stray `*` (the "song missing from playlist" icon) on every song line once `JMK_MODE`'s
   `hasTrack` check had set it once.** The original's `reset_playlist_counts()` doubled as
   "clear this icon flag" every time it ran (on a fresh match or an ordinary clear); the refactor
   dropped that coupling, assuming it was safe display-only plumbing, and only handled the one
   "smart-shuffle exception" case that sets the flag - so nothing ever cleared it again once set.
   Fixed by giving `PlaylistTracker` an `on_reset` callback, invoked every time `reset_counts()`
   runs, wired back to the original's icon-clearing behavior.

Both are fixed. Re-running `compare_with_original.py` shows all 5 sequences producing
byte-identical notification output between the original and refactored code (modulo timestamps).

## A deliberate improvement (not a regression): "Cleared" now reaches the screen

While reviewing this output, a third issue came up that predates the refactor entirely: the
*original* code never printed a screen line for the most common "cleared" case (an ordinary
end-of-tolerance clear, as opposed to the two rarer "switched to a different playlist" cases,
which already printed one). The real notification (email/push/spreadsheet) always fired
correctly either way - only the console/log line was missing. Since this was pointed out as
worth fixing rather than just documenting, the refactored code now also prints that line, via
the same "print eagerly, before `reset_counts()` clears it" mechanism the other two cases already
used. This is an intentional divergence from the original's console output (not from its real
notifications), confirmed working end-to-end below.

## Sample output

`SEQUENCE_DETECT_THEN_CLEAR` (from `demo_fixtures.py`, since none of the original 5 sequences
complete a full cycle) against the refactored code - 3 songs from the synthetic "Test Playlist"
in a row (`qty_start=3`) → **Detected**, one tolerated off-list song, then a second off-list song
(`qty_end=2`) → **Cleared**, both now visible on screen:

```
09/20, 21:27:44: , *** Start notification sent
09/20, 21:27:44: , [00] Umbrella - Rihanna (Good Girl Gone Bad) [Today's Top Hits]
09/20, 21:27:44: , [03] Love On The Brain - Rihanna (Anti) [Today's Top Hits]
09/20, 21:27:44: , [06] Umbrella <3 - Rihanna (Good Girl Gone Bad) [Test Playlist]
09/20, 21:27:44: , [06] *** Playlist 'Test Playlist' Detected
09/20, 21:27:44: , [09] Beyond - Leon Bridges (Beyond) [Test Playlist]*
09/20, 21:27:44: , [12] Texas Sun - Khruangbin (Texas Sun)
09/20, 21:27:44: , [12] *** Playlist 'Test Playlist' Cleared, Song Count: 3
09/20, 21:27:44: , [15] Love On The Brain - Rihanna (Anti) [Today's Top Hits]
```

Notification calls captured during that same run:

```
type='active'   START: Umbrella - Rihanna (Good Girl Gone Bad) [Today's Top Hits]
type='song'     [00] Umbrella - Rihanna (Good Girl Gone Bad) [Today's Top Hits]
type='song'     [03] Love On The Brain - Rihanna (Anti) [Today's Top Hits]
type='detected' *** Playlist 'Test Playlist' Detected: Umbrella <3 - Rihanna (Good Girl Gone Bad) [Test Playlist]
type='song'     [06] Umbrella <3 - Rihanna (Good Girl Gone Bad) [Test Playlist]
type='song'     [09] Beyond - Leon Bridges (Beyond) [Test Playlist]*
type='cleared'  *** Playlist 'Test Playlist' Cleared: Texas Sun - Khruangbin (Texas Sun) - Song Count: 3
type='song'     [12] Texas Sun - Khruangbin (Texas Sun)
type='song'     [15] Love On The Brain - Rihanna (Anti) [Today's Top Hits]
```

Running this same sequence against the *original* codebase fires the identical `notification:`
calls (both `detected` and `cleared` reach real notification channels there too), but its console
transcript never prints the `*** Playlist 'Test Playlist' Cleared` line - confirming this is the
one deliberate, requested difference from the original, not an accident.

For the 5 original `test_fixtures.py` sequences (which only ever reach **Detected**, for the
reason above), `compare_with_original.py`'s notification-level check remains the primary
regression signal, and it still reports all 5 as matching.

## Re-running this check

```
cd test_playlist_detection
python compare_with_original.py
```

Expected output: `ALL SEQUENCES MATCH`. If a future change to the playlist-detection code makes
this print `SOME SEQUENCES DIFFER`, that's either a regression or an intentional behavior change
that needs the same kind of review this document describes - not something to wave through.

To see the full detect-then-clear cycle (including the "Cleared" screen line):

```
python run_against_target.py .. SEQUENCE_DETECT_THEN_CLEAR 14
```
