"""
End-to-end scenario tests for the monitored-playlist detection feature (PlaylistTracker /
ADD_PLAYLISTS_TO_MONITOR in spotify_monitor.py). Drives the real spotify_monitor_friend_uri()
loop against synthetic friend data (see playlist_harness.py) and asserts, for every song
observed, exactly which ones show the playlist tag, the smart-shuffle icon, and a
Detected/Cleared message - and that nothing shows up anywhere it shouldn't.

These were previously checked by eye against manually-run scripts in ../test_playlist_detection/;
this file turns the same scenarios into assertions pytest runs automatically.
"""
import pytest

import time as real_time

import spotify_monitor as monitor
from playlist_harness import PlaylistSession, absent, build_sequence, song


def make_playlist(name="Test Playlist", qty_start=3, qty_end=2, icon="<3", notify=True, override=False, tracks=("SONGA", "SONGB")):
    # find_song_in_playlists() matches f"{sp_artist} - {sp_track}".upper() against tracks_set - all
    # our synthetic songs use artist "Artist", so a bare "SONGA" must become "ARTIST - SONGA" here.
    return {
        "name": name, "filename": "", "qty_start": qty_start, "qty_end": qty_end,
        "url": "http://playlist", "icon": icon, "notify": notify, "override": override, "refresh": 0,
        "tracks_set": {f"ARTIST - {t}" for t in tracks},
        "count_start": 0, "count_end": 0, "count_shuffle": 0,
    }


def assert_tagged_exactly(session, expected_offsets):
    """Every song at one of expected_offsets shows the playlist tag; every other song doesn't."""
    records = session.song_records()
    assert records, "no song lines were parsed out of the console output"
    for r in records:
        expected = r["offset"] in expected_offsets
        actual = r["playlist"] == session.playlist_name
        assert actual == expected, (
            f"offset {r['offset']} ({r['track']}): expected playlist tag={expected}, got {r['playlist']!r}"
        )


def assert_icon_add_exactly(session, expected_offsets):
    records = session.song_records()
    for r in records:
        expected = r["offset"] in expected_offsets
        assert r["icon_add"] == expected, (
            f"offset {r['offset']} ({r['track']}): expected shuffle-icon={expected}, got {r['icon_add']}"
        )


def assert_events_exactly(session, detected_at=(), cleared_at=()):
    assert session.detected_offsets() == list(detected_at), (
        f"Detected fired at {session.detected_offsets()}, expected {list(detected_at)}"
    )
    assert session.cleared_offsets() == list(cleared_at), (
        f"Cleared fired at {session.cleared_offsets()}, expected {list(cleared_at)}"
    )


def assert_start_notification_precedes_final_detected(session):
    """The (re-announced) Detected line must read as part of the new session, after its own
    "Start notification sent" banner - not before it, as if it belonged to the session that just
    ended. Regression guard for a real bug: the "friend resumed after being offline" code path
    used to print this Detected re-announcement before printing "Start notification sent"."""
    start_idx = session.output.rindex("Start notification sent")
    detected_idx = session.output.rindex("Detected")
    assert start_idx < detected_idx, (
        "the new session's 'Start notification sent' banner must print before its Detected re-announcement"
    )


# --- Scenario 1: first song is already on the playlist, but shouldn't be announced yet ---
def test_first_song_on_playlist_does_not_announce(monkeypatch):
    seq = build_sequence(["SONGA"])
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=3)
    assert_tagged_exactly(session, expected_offsets=set())
    assert_icon_add_exactly(session, expected_offsets=set())
    assert_events_exactly(session, detected_at=(), cleared_at=())


# --- Scenario 2: the full documented cycle ---
# build_sequence() spaces songs 180 real seconds (3 minutes) apart, and the console's "[NN]"
# marker is minutes elapsed since the session started (time_diff_str()) - so with a 3-minute
# step, song index N lands on minute-marker 3*N.
def test_full_detect_shuffle_clear_cycle(monkeypatch):
    seq = build_sequence([
        "OFFLIST1",        # [00] not on playlist - count stays at 0
        "SONGA",           # [03] 1/3
        "SONGB",           # [06] 2/3
        "SONGA",           # [09] 3/3 -> Detected
        "SONGB",           # [12] still in playlist
        "SONGA",           # [15] still in playlist
        "OFFLIST2",        # [18] 1st miss (qty_end=2) -> tolerated, shows tag + icon
        "OFFLIST3",        # [21] 2nd miss -> Cleared
        "OFFLIST4",        # [24] no longer tracked
        "OFFLIST5",        # [27] no longer tracked
    ])
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=12)
    assert_tagged_exactly(session, expected_offsets={9, 12, 15, 18})
    assert_icon_add_exactly(session, expected_offsets={18})
    assert_events_exactly(session, detected_at=(9,), cleared_at=(21,))


# --- Scenario 3: a custom icon (including an extended/Unicode one) is embedded on matched songs,
# distinct from the generic ICON_SONG_MISSING_FROM_PLAYLIST ("*") shown on shuffle-tolerance songs ---
@pytest.mark.parametrize("icon", [" <3", " ♥"])
def test_custom_icon_shown_on_matched_songs_not_on_shuffle_songs(monkeypatch, icon):
    seq = build_sequence(["SONGA", "SONGB", "SONGA", "OFFLIST1"])  # offsets: 0, 3, 6, 9
    session = PlaylistSession(monkeypatch, make_playlist(icon=icon), seq, iterations=6)
    records = {r["offset"]: r for r in session.song_records()}
    assert records[6]["track"] == f"SONGA{icon}", "the confirmed/matched song should carry the custom icon"
    assert records[9]["track"] == "OFFLIST1", "an off-list (shuffle-tolerance) song should NOT carry the custom icon"
    assert records[9]["icon_add"] is True, "the shuffle-tolerance song should carry the generic '*' instead"
    assert_events_exactly(session, detected_at=(6,), cleared_at=())


# --- Regression: a song can genuinely belong to both the playlist Spotify reports as current
# context AND a separately-monitored playlist (e.g. a friend's own playlist that happens to
# include songs also saved to Discovery Zone) - Spotify confirming the reported playlist must not
# disqualify the song from also counting toward a monitored playlist it's actually on ---
def test_song_confirmed_in_a_different_reported_playlist_still_counts_toward_a_monitored_one(monkeypatch):
    # search_playlist_result=True simulates Spotify's own search confirming these songs really are
    # in "My Playlist" - previously this alone made hasTrack=True and short-circuited detection
    # entirely, even though SONGA/SONGB are also on "Test Playlist"'s own track list.
    seq = build_sequence([("SONGA", "My Playlist"), ("SONGB", "My Playlist"), ("SONGA", "My Playlist")])
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=6, search_playlist_result=True)
    assert_tagged_exactly(session, expected_offsets={6})
    assert_events_exactly(session, detected_at=(6,), cleared_at=())


def test_song_confirmed_only_in_a_different_playlist_does_not_count_toward_monitored_one(monkeypatch):
    # Control for the test above: songs that are ONLY in the reported "My Playlist" (not on Test
    # Playlist's track list at all) must still be left alone - the fix must not loosen matching
    # into "anything Spotify confirms in any playlist counts everywhere".
    seq = build_sequence([("OFFLIST1", "My Playlist"), ("OFFLIST2", "My Playlist"), ("OFFLIST3", "My Playlist")])
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=6, search_playlist_result=True)
    assert_tagged_exactly(session, expected_offsets=set())
    assert_events_exactly(session, detected_at=(), cleared_at=())


# --- Regression: real production bug - a song reported under an unrelated playlist name that
# Spotify's own search does NOT confirm (search_playlist_result stays at its default False) must
# still be recognized as belonging to a monitored playlist it's genuinely on, while still counting
# up toward Detected (not yet tagged/shown with the shuffle icon, exactly like Scenario 1) - not
# flagged with the "*" shuffle icon or an "ERROR: NOT FOUND" log line, both of which wrongly imply
# the song is off-list when it's actually a normal, still-counting-up match ---
def test_song_not_confirmed_by_spotify_search_but_on_monitored_list_is_not_flagged_as_an_error(monkeypatch):
    seq = build_sequence([("SONGA", "Liked Songs"), ("SONGB", "Liked Songs"), ("SONGA", "Liked Songs")])
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=6)
    assert_icon_add_exactly(session, expected_offsets=set())
    assert_events_exactly(session, detected_at=(6,), cleared_at=())
    assert "NOT FOUND" not in session.log_output, (
        "a song genuinely on the monitored playlist's track list must not be logged as an error "
        "just because it isn't confirmed under a different, unrelated reported playlist name"
    )


# --- Regression: real production bug - once a detected playlist is cleared because Spotify
# confirms the song genuinely belongs to a different, unrelated playlist (hasTrack=True), its
# counters must be fully reset, not preserved. PlaylistTracker.advance()'s has_track branch used to
# call reset_counts(self.previous['name']) - "protecting" the exact playlist it had just decided to
# clear, so count_start was never actually reset. The playlist would silently reappear as "matched"
# a few songs later without ever passing through a fresh qty_start count-up, and without a new
# "Detected" ever firing again (count_start had already sailed past qty_start, unnoticed).
#
# Design change (later, by request): a has_track=True song no longer instantly clears - it now
# costs the playlist one ordinary miss toward qty_end, same as an unconfirmed off-list song, so a
# single such song is tolerated (default qty_end=2) and only a second one in a row actually clears.
# The reset-on-clear behavior above still applies once that threshold is reached ---
def test_cleared_via_has_track_resets_counts_and_requires_a_fresh_detection(monkeypatch):
    seq = build_sequence(["SONGA", "SONGB", "SONGA", "OFFLIST1", "OFFLIST2", "SONGA", "SONGB", "SONGA"])
    # search_playlist_result=True: OFFLIST1/OFFLIST2 (not on Test Playlist's own list) get
    # hasTrack=True, genuinely confirmed elsewhere - the trigger for the has_track miss-counting path.
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=16, search_playlist_result=True)
    # Detected twice - once for the first SONGA/SONGB/SONGA run, and again for the one after clearing
    # - proving a fresh 3-song count-up was required the second time, not an instant match. Cleared
    # only after the SECOND has_track song (qty_end=2): the first one alone must be tolerated, not
    # treated as an instant clear.
    assert_events_exactly(session, detected_at=(6, 21), cleared_at=(12,))
    assert monitor.monitored_playlists_data["Test Playlist"]["count_start"] == 3, (
        "count_start must reflect only the second SONGA/SONGB/SONGA run - if the clear didn't "
        "really reset it, this would be 6 (3 preserved from before + 3 more piled on top)"
    )


# --- Regression: real production bug - when the very first song observed after a friend resumes
# from being idle also triggers a real Detected/Cleared through the NORMAL per-song
# tracker.advance() call (not the separate "already-detected, re-announce" check), that message
# used to print before "Start notification sent" for the new session - the normal call always runs
# structurally earlier in the code than the "friend resumed" block that prints the banner, and
# advance() prints its own detected/cleared line eagerly (so a later reset_counts() in the same
# call can't wipe it unseen). Fixing the has_track/exception-branch "Cleared" gates earlier this
# session made this reachable in practice, since those branches previously never got a chance to
# announce anything at all here.
#
# qty_end=1 here (instead of the usual default of 2) so the single off-list song that resumes the
# session is, by itself, enough to cross the miss threshold and fire "Cleared" - exercising the
# exact same generic miss-counting path (see the has_track qty_end redesign above) on the very first
# song of a new session, which is what originally exposed the print-ordering bug ---
def test_resumed_session_clear_prints_after_start_notification(monkeypatch):
    base = int(real_time.time())
    seq = [
        (song("SONGA", 0, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base),
        (song("SONGB", 180, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 180),
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 360),  # 3/3 -> Detected
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 450),  # idle detected here
        # Resumes on a song Spotify confirms belongs to a different, unrelated playlist - this
        # triggers the has_track miss-counting path on the very same song that starts the new
        # session, and (with qty_end=1 below) crosses the threshold on that first miss.
        (song("OFFLIST1", 600, "Some Other Playlist", "spotify:playlist:otherplaylist", base), base + 610),
    ]
    session = PlaylistSession(monkeypatch, make_playlist(qty_end=1), seq, iterations=20, inactivity_check_seconds=60,
                               search_playlist_result=True)
    assert "got ACTIVE after being offline" in session.log_output, "the resume itself must actually fire"
    start_idx = session.output.rindex("Start notification sent")
    cleared_idx = session.output.rindex("Cleared")
    assert start_idx < cleared_idx, (
        "the new session's 'Start notification sent' banner must print before a Cleared line "
        "triggered by that same first song, not after"
    )


# --- Regression: real production bug - a friend who shows offline/stale at boot must not have
# their last-known song counted twice: once by LOOP A's silent boot-time snapshot (which used to
# run unconditionally, even for an offline friend), and again moments later when they resume and
# Spotify reports that same still-playing track with a fresh activity timestamp (LOOP C's
# track_changed check compares only that timestamp, not track identity, so a same-track-newer-
# timestamp sample reads as a brand new song). Detection must require the full qty_start distinct
# songs, not qty_start - 1, when this happens ---
def test_stale_boot_song_is_not_double_counted_on_resume(monkeypatch):
    base = int(real_time.time())
    seq = [
        # Boot sample: SONGA's own reported timestamp is old (offset 0), but the clock is already
        # far ahead (+700s) when this is served, so cur_ts - sp_ts (700s) exceeds the 60s inactivity
        # threshold - the friend must appear offline/stale at boot, not active.
        (song("SONGA", 0, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 700),
        # Friend resumes on the SAME track - a fresh reported timestamp (offset 700) for a track
        # that's identical to the stale boot sample.
        (song("SONGA", 700, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 700),
        (song("SONGB", 880, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 880),
        (song("SONGC", 1060, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 1060),
    ]
    session = PlaylistSession(monkeypatch, make_playlist(tracks=("SONGA", "SONGB", "SONGC")), seq,
                               iterations=20, inactivity_check_seconds=60)
    playlist = monitor.monitored_playlists_data[session.playlist_name]
    # Exactly 3 distinct on-list songs (resumed SONGA, SONGB, SONGC) - not 4 (SONGA counted twice).
    assert playlist["count_start"] == 3, f"SONGA must count once on resume, not once at boot AND once on resume, got count_start={playlist['count_start']}"
    # Detected must land on SONGC (the 3rd distinct song), not SONGB (which it would incorrectly
    # reach if the boot sample had already banked an extra, phantom count).
    songc_offset = next(r["offset"] for r in session.song_records() if r["track"].startswith("SONGC"))
    assert_events_exactly(session, detected_at=(songc_offset,), cleared_at=())


# --- Regression: real production bug - a monitored playlist can cross its own qty_start threshold
# while it's the "exception" playlist for a DIFFERENT monitored playlist that's still within its
# own miss tolerance (PlaylistTracker.advance()'s "SONG EXCEPTION BUT IN ANOTHER MONITORED
# PLAYLIST" branch). That branch used to increment the exception playlist's count_start without
# ever checking whether the increment crossed its threshold, so the crossing went completely
# unannounced - the playlist became tagged/"matched" a song later, with no Detected message ever
# having fired ---
def test_playlist_detected_via_exception_branch_while_a_second_playlist_still_counting_up(monkeypatch):
    # Two playlists so the "previous playlist still tolerating misses" exception path is reachable:
    # qty_end is set generously high on both so neither clears mid-test.
    playlist_a = make_playlist(name="Test Playlist", qty_start=3, qty_end=5, tracks=("SONGX", "SONGX2", "SONGX3", "SONGX4"))
    playlist_b = make_playlist(name="Other Playlist", qty_start=3, qty_end=5, tracks=("SONGY",))
    seq = build_sequence([
        ("SONGX", "Some Context"),   # Test Playlist: count_start 0 -> 1
        ("SONGX2", "Some Context"),  # Test Playlist: count_start 1 -> 2
        ("SONGY", "Some Context"),   # Other Playlist becomes current (Test Playlist still tolerating misses)
        ("SONGX3", "Some Context"),  # Test Playlist is current again, as an exception to Other Playlist
                                      # (which hasn't hit its own qty_start) - count_start 2 -> 3 = qty_start
        ("SONGX4", "Some Context"),  # an ordinary continuation, now clearly past threshold
    ])
    session = PlaylistSession(monkeypatch, [playlist_a, playlist_b], seq, iterations=8)
    # Detected must fire on SONGX3 - the exact song whose count crossed qty_start - not on SONGX4
    # (where the old code first noticed the count was already past threshold) and not never at all.
    songx3_offset = next(r["offset"] for r in session.song_records() if r["track"].startswith("SONGX3"))
    assert_events_exactly(session, detected_at=(songx3_offset,), cleared_at=())
    assert monitor.monitored_playlists_data["Test Playlist"]["count_start"] == 4


# --- Scenario 4a: the friend goes idle (same track, no updates) and later becomes active again
# with a new on-list track - every count/tag for the monitored playlist must survive the gap ---
def test_state_survives_going_idle_then_active_with_on_list_song(monkeypatch):
    base = int(real_time.time())
    seq = [
        (song("SONGA", 0, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base),
        (song("SONGB", 180, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 180),
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 360),  # 3/3 -> Detected
        # friend goes idle: same track repeats while the (mocked) clock keeps advancing past the
        # 60s inactivity threshold, without a single new song being observed
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 380),
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 450),  # idle detected here
        # friend becomes active again with a new on-list song
        (song("SONGB", 600, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 610),
        (song("SONGA", 780, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 790),
    ]
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=20, inactivity_check_seconds=60)
    playlist = monitor.monitored_playlists_data[session.playlist_name]

    # Proves the idle->active transition itself actually fired (the "went inactive" / "resumed
    # after offline" code paths), not just that nothing disruptive happened to the counters. Both
    # print() bare, not via print_to_screen(), so they land in the log file, not session.output -
    # see the comment on PlaylistSession's log_output capture in playlist_harness.py.
    assert "got INACTIVE" in session.log_output, "the idle gap must actually trigger the inactivity check"
    assert "got ACTIVE after being offline" in session.log_output, "resuming must actually trigger the offline-resume check"

    # A fresh "session" boot (the friend becoming active again) re-announces Detected for a
    # playlist that already met the threshold before the gap - this matches the original code's
    # own "needed to cause detection messaging when user becomes active and already on a detected
    # playlist" boot check, so a second Detected at the new session's offset 0 is expected here,
    # not a regression.
    assert_events_exactly(session, detected_at=(6, 0), cleared_at=())
    assert_start_notification_precedes_final_detected(session)
    records = {r["offset"]: r for r in session.song_records()}
    # time_diff_str() counts from the new session's own start after resuming, so the post-gap
    # songs land at 0 and 3 rather than 10 and 13.
    for offset in (6, 0, 3):
        assert offset in records, f"no song line recorded at offset {offset}"
    assert records[0]["playlist"] == session.playlist_name, "tag must survive the idle gap (SONGB after resuming)"
    assert records[3]["playlist"] == session.playlist_name, "tag must still show on the next song too"
    # the underlying counters must have kept accumulating, not reset by the idle gap
    assert playlist["count_start"] >= 5, f"count_start should keep growing across the gap, got {playlist['count_start']}"
    assert playlist["count_end"] == 0, "no off-list songs occurred, so count_end must still be 0"
    assert session.notifications_of_type("cleared") == [], "must not have cleared just from going idle"


def test_state_survives_going_idle_then_shuffle_then_clear(monkeypatch):
    base = int(real_time.time())
    seq = [
        (song("SONGA", 0, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base),
        (song("SONGB", 180, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 180),
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 360),  # 3/3 -> Detected
        (song("SONGA", 360, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 450),  # idle detected here
        # resumes with an OFF-list song: tolerated (qty_end=2), shows tag + icon
        (song("OFFLIST1", 600, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 610),
        # a second off-list song clears it
        (song("OFFLIST2", 780, "Today's Top Hits", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", base), base + 790),
    ]
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=20, inactivity_check_seconds=60)
    records = {r["offset"]: r for r in session.song_records()}

    assert "got INACTIVE" in session.log_output, "the idle gap must actually trigger the inactivity check"
    assert "got ACTIVE after being offline" in session.log_output, "resuming must actually trigger the offline-resume check"

    # A fresh session boot re-announces Detected for a playlist that already met the threshold
    # before the gap (see the sibling idle test above for why offset 0 here is expected, not a
    # regression); time_diff_str() then counts from this new session's own start, so the tolerated
    # shuffle song and the clearing song land at 0 and 3 rather than 10 and 13.
    assert_events_exactly(session, detected_at=(6, 0), cleared_at=(3,))
    assert_start_notification_precedes_final_detected(session)
    assert records[0]["playlist"] == session.playlist_name and records[0]["icon_add"] is True, (
        "the off-list song right after resuming from idle should still be a tolerated shuffle exception"
    )
    # once cleared, our tag must not show - Spotify's own "Today's Top Hits" context (unrelated
    # to the monitored playlist) is what's reported instead, which is correct, not our tag leaking
    assert records[3]["playlist"] != session.playlist_name, "once cleared, our tag must not show"
    assert records[3]["icon_add"] is False, "once cleared, the shuffle icon must not show either"


# --- Scenario 4b: friend disappears from the friends list mid-session and later reappears -
# playlist state must survive the gap and keep behaving correctly once songs resume ---
def test_state_survives_friend_disappearing_and_reappearing_on_list(monkeypatch):
    seq = build_sequence(["SONGA", "SONGB", "SONGA"]) + [absent()] * 4 + build_sequence(["SONGB"], step_seconds=180)
    # stitch the second build_sequence's single fresh-"now"-based timestamp onto the tail; what
    # matters is only that it's a new, later timestamp for the same on-list track
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=14)
    detected = session.detected_offsets()
    assert len(detected) == 1, f"expected exactly one Detected, got {detected}"
    # after reappearing, the next on-list song must still show the tag and not re-announce Detected
    records = session.song_records()
    assert records, "no song lines parsed"
    assert records[-1]["playlist"] == session.playlist_name, "playlist tag must persist across the gap"
    assert session.cleared_offsets() == [], "should not have cleared just from a friends-list gap"


def test_state_survives_disappearing_then_clears_on_return(monkeypatch):
    seq = build_sequence(["SONGA", "SONGB", "SONGA"]) + [absent()] * 4 + build_sequence(["OFFLIST1", "OFFLIST2"], step_seconds=180)
    session = PlaylistSession(monkeypatch, make_playlist(), seq, iterations=16)
    assert len(session.detected_offsets()) == 1
    assert len(session.cleared_offsets()) == 1, "two off-list songs after returning should still clear (qty_end=2)"


# --- Scenario 5: override jump-starts detection on the very first sample, instead of after qty_start in a row ---
def test_override_detects_on_first_sample(monkeypatch):
    seq = build_sequence(["SONGA"])
    session = PlaylistSession(monkeypatch, make_playlist(override=True), seq, iterations=3)
    assert_tagged_exactly(session, expected_offsets={0})
    assert_events_exactly(session, detected_at=(0,), cleared_at=())


def test_override_false_does_not_jump_start(monkeypatch):
    seq = build_sequence(["SONGA"])
    session = PlaylistSession(monkeypatch, make_playlist(override=False), seq, iterations=3)
    assert_tagged_exactly(session, expected_offsets=set())
    assert_events_exactly(session, detected_at=(), cleared_at=())


# --- Scenario 6: notify=False suppresses the real notification channel, but the screen/tag/
# Detected-Cleared text is unaffected (that's controlled by the session, not the per-playlist flag) ---
def test_notify_false_suppresses_real_notification_but_not_screen_text(monkeypatch):
    seq = build_sequence(["SONGA", "SONGB", "SONGA"])  # offsets: 0, 3, 6
    session = PlaylistSession(monkeypatch, make_playlist(notify=False), seq, iterations=6)
    assert_events_exactly(session, detected_at=(6,), cleared_at=())
    assert session.notifications_of_type("detected") == [], "notify=False must suppress the real notification"


def test_notify_true_sends_real_notification(monkeypatch):
    seq = build_sequence(["SONGA", "SONGB", "SONGA"])  # offsets: 0, 3, 6
    session = PlaylistSession(monkeypatch, make_playlist(notify=True), seq, iterations=6)
    assert_events_exactly(session, detected_at=(6,), cleared_at=())
    assert len(session.notifications_of_type("detected")) == 1, "notify=True must send the real notification"


# --- Config validation ---
class TestValidateAddPlaylistsToMonitor:
    @pytest.fixture(autouse=True)
    def _silence_error_output(self, monkeypatch):
        # validate_add_playlists_to_monitor() reports errors via print_to_both(), which needs a
        # real log_logger (normally set up by main()/PlaylistSession) - not relevant to what these
        # tests check (the filtered return value), so just swallow the printed text.
        monkeypatch.setattr(monitor, "print_to_both", lambda message: None)

    def _base(self, **overrides):
        cfg = {"name": "P", "filename": "f.txt", "qty_start": 3, "qty_end": 2}
        cfg.update(overrides)
        return cfg

    def test_valid_entry_is_kept(self):
        result = monitor.validate_add_playlists_to_monitor([self._base()])
        assert len(result) == 1

    def test_real_world_config_is_kept(self):
        real_config = [
            {"name": "Discovery Zone", "filename": "_config_and_logs/dz_songs.txt", "qty_start": 3, "qty_end": 2,
             "refresh": 3600, "icon": " ♥", "override": True, "notify": True,
             "url": "https://open.spotify.com/playlist/5eEkzONtwQsK6efRldsyoI"},
            {"name": "Liked Songs", "filename": "_config_and_logs/liked_songs_jmk.txt", "qty_start": 3, "qty_end": 2,
             "refresh": 3600, "override": True, "notify": True, "url": "Liked Songs (no URL)"},
        ]
        result = monitor.validate_add_playlists_to_monitor(real_config)
        assert [p["name"] for p in result] == ["Discovery Zone", "Liked Songs"]

    @pytest.mark.parametrize("overrides", [
        {"name": ""},
        {"name": 123},
        {"filename": ""},
        {"filename": None},
        {"qty_start": "three"},
        {"qty_start": 0},
        {"qty_start": -1},
        {"qty_end": 0},
        {"qty_end": True},  # bool is not an acceptable int here even though bool subclasses int
        {"override": "yes"},
        {"notify": 1},
        {"refresh": -5},
        {"refresh": 99_999_999},
        {"refresh": "3600"},
        {"url": 5},
        {"icon": 5},
    ])
    def test_invalid_entry_is_dropped(self, overrides):
        result = monitor.validate_add_playlists_to_monitor([self._base(**overrides)])
        assert result == []

    def test_non_dict_entry_is_dropped(self):
        assert monitor.validate_add_playlists_to_monitor(["not a dict", 5, None]) == []

    def test_duplicate_names_second_one_dropped(self):
        result = monitor.validate_add_playlists_to_monitor([self._base(name="Dup"), self._base(name="Dup", filename="g.txt")])
        assert len(result) == 1
        assert result[0]["filename"] == "f.txt"

    def test_one_bad_entry_does_not_affect_others(self):
        result = monitor.validate_add_playlists_to_monitor([self._base(name="Good"), self._base(name="Bad", qty_start=0)])
        assert [p["name"] for p in result] == ["Good"]

    def test_zero_refresh_is_valid(self):
        # 0 explicitly means "don't reload" - not an error
        result = monitor.validate_add_playlists_to_monitor([self._base(refresh=0)])
        assert len(result) == 1

    def test_unknown_key_is_tolerated_not_rejected(self):
        result = monitor.validate_add_playlists_to_monitor([self._base(some_future_field="x")])
        assert len(result) == 1
