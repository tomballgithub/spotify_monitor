"""
Runs every SEQUENCE_* in test_fixtures.py through run_against_target.py against two
spotify_monitor.py codebases (this repo and a comparison "original" one) and diffs the
resulting notification text, to check whether a change to the playlist-detection code altered
observable behavior. Timestamps are normalized out before comparing, since two separate process
runs a moment apart will otherwise never match exactly.

Usage:
    python compare_with_original.py [path-to-original-spotify_monitor-directory]

Defaults to comparing against C:\\Python Dev\\spotify_monitor if no path is given.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFACTORED_DIR = HERE.parent
ORIGINAL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\Python Dev\spotify_monitor")

SEQUENCES = [
    "SEQUENCE_SONG_CHANGE",
    "SEQUENCE_STEADY",
    "SEQUENCE_TWO_CHANGES",
    "SEQUENCE_DISCOVERY_ZONE_DETECT",
    "SEQUENCE_LIKED_SONGS_DETECT",
]
ITERATIONS = 12
TS_RE = re.compile(r"\d{2}/\d{2}, \d{2}:\d{2}:\d{2}")


def run(target_dir, sequence):
    result = subprocess.run(
        [sys.executable, str(HERE / "run_against_target.py"), str(target_dir), sequence, str(ITERATIONS)],
        capture_output=True, text=True,
    )
    lines = [line for line in result.stdout.splitlines() if "notification:" in line]
    return "\n".join(TS_RE.sub("TIMESTAMP", line) for line in lines)


if __name__ == "__main__":
    print(f"Refactored: {REFACTORED_DIR}")
    print(f"Original:   {ORIGINAL_DIR}")
    print()
    all_matched = True
    for sequence in SEQUENCES:
        old_out = run(ORIGINAL_DIR, sequence)
        new_out = run(REFACTORED_DIR, sequence)
        if old_out == new_out:
            print(f"[MATCH]   {sequence}")
        else:
            all_matched = False
            print(f"[DIFFERS] {sequence}")
            print("  --- original ---")
            print("\n".join(f"  {line}" for line in old_out.splitlines()))
            print("  --- refactored ---")
            print("\n".join(f"  {line}" for line in new_out.splitlines()))
    print()
    print("ALL SEQUENCES MATCH" if all_matched else "SOME SEQUENCES DIFFER - see above")
