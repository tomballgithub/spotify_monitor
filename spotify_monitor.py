# Any DZ song should always get a heart
# Discovery Zone says (custom)(unique) [ignore those on detected playlists]

# some items have  ♥ ♥
# alerts on bedroom playlists?
# always add icon if theres a match
# option on whether to count up during search for playlist

# should always cause an asteriks#
# ERROR: track: Umbrella, NOT FOUND in playlist: And, baby, that’s show business for you ❤️‍🔥 (Umbrella)

# found_playlist['

# count_end
# qty_end
# count_start
# qty_start
# playlist name
# count_shuffle

# count_overridden
# icon_add
# new_playlist

# _detected
# _cleared

# dz_message = ""
# dz_msg_screen = ""
# body_dz = ""
# body_dz_html = ""

# jmk_send = False
# found_playlist = False
# last_found_playlist = False
# active_ever = False
# icon_add = False
# playlist_suffix_string = ""
# hasTrack = False
# sp_playlist_owner = ""
# sp_playlist_image_url = ""        

# monitored_playlists_data = {}
# DEBUG_JMK = False
# count_overridden = False
# icon if found in playlist or not?

# notify if sp_dc error
# write song info straight to google sheet
# option to notify for all email types
# generatic notifcation and print strings real time instead of storing strings?
# do this centrally? sp_track = sp_track + found_playlist.get('icon', '')
# switching from DZ to actual playlist doesnt 'cleared'
# don't assume spotify playlist has song - I saw this broken yesterday - Party Mix instead of liked songs
# - hastrack = search playlist not working for Party Mix
# - because it is custom to the person
# - is it viable to still track count_start and if it gets to limit than its good?
#
# improve comments and delete old code
# add # of sessions - need check on profile_monitor if # of songs changes by 100+/- to filter that out
# should DZ count be capped at listening song cap (or at least clarify it never resets)

# rearchitect my playlist monitoring PR tracking/counting/messaging? (it's convoluted)
# variables to indicate in a playlist, which one, first time loading, first time starting?, detected SMS/email, cleared SMS/email state
# centralize processing?
# - song strings for each song to screen
# - detected to screen/email
# - cleared to screen/email

# only show after first? or if at startup retry? * Error, retrying in 3 minutes: Failed to obtain a valid Spotify access token after 3 attempts: refresh_access_token_from_sp_dc(): Unsuccessful token request: 400 Client Error: Bad Request for url: https://open.spotify.com/api/token?reason=init&productType=web-player&totp=577757&totpServer=577757&totpVer=0&sTime=1753718266&cTime=1753718265688&buildDate=2025-07-28&buildVer=web-player_2025-07-28_1753718266000_016bf795
# -* Error: sp_dc may be invalid/expired or Spotify has broken sth again!

# design & try test cases - test transitioning from one playlist to another (given I zero everything out)
# - compare old to new, screen view, emails, etc
#
#?? change NTFY resized image hosting to krontz.nakattack.com to avoid Microsoft filtering
#?? added playlist on 'detected' NTFY messages
#?? add icons to start and stop NTFY essages
#?? clear sp_playlist_image_url if not a playlist
#?? listened_songs was showing -1 on NTFY stream updates
#?? Send full stream via NTFY
#?? Use NTFY for notifications including locally hosted image of the album or song
#?? Dz count shouldnt be 4 after 1st dong
#?? if it's a real playlist and song is in it, that takes priority? (ex: Soft 10s (custom), Rihanna - Love On The Brain) - startup problem?
#?? reset override count when streaming stops permanently (not inactive))
#?? custom/unique tag do it differently
#?? playlists not in email - also incorrect today with two different names
#?? protect new playlist count while expiring old one
#?? fixed active_ever
#?? prioritize playlist exact name match check in find_song_in_playlists
#?? put * on Liked Songs in emails/logs if *
#?? build_dz ONLY if count is high enough to start - errant playlist counts in emails/log (DZ_MESSAGE(4a))
#?? don't show cleared message/sms IFF first boot (never active) AND inactive
#?? fixed missing cleared messages and added more debug to track how code operates
#?? abort loading periodic playlist is length changes by > MAX_PLAYLIST_DIFFERENTIAL 
#?? use nonlocal within reset_playlist_counts to adjust variables up-level - every email has Song Count: 1 for liked songs
#?? don't show playlist cleared if user just starting up
#?? removed active user check near SONG NOT IN A MONITORED PLAYLIST (2) since IN A PLAYLIST didn't have that same check
#?? playlist name match mean automatic switch to new playlist? (better if name just changed?)
#?? missing 'detected' after KARA becomes active  (first time or every time?)
#?? fixed count messages in log email -> was sometimes this -> # *** Playlist 'Liked Songs' Cleared: Don't - Bryson Tiller (T R A P S O U L) - Song Count: 8
#?? fixed errant case of * playlist assignment (also added a SPECIAL CASE2 debug message)
#?? fixed missing * on emails
#?? only override count if < than qty_start (don't go backwards)
#?? fix duplicate 'cleared' messages
#?? fix incorrect DZ count shown in emails
#?? show song count on END texts
#?? change wording of the message to indicate it's a playlist that was detected -> #*** Liked Songs Detected
#?? change wording of the email 'counts' to indicate it's a playlist that was counted rather than Liked Songs Count: XX
#?? properly handle case of exception song is from a different monitored playlist
#?? and in above case force '*** cleared' message
#?? track smart shuffle count and show it if > 0 when showing DZ song count
#?? removed count on 'detected' texts and fixed count always being 0 for 'cleared' texts
#?? need to allow exception while counting up because otherwise may never get there if '3'
#?? correctly match playlist name in find_song_in_playlists by sending sp_playlist
#?? clearer debug to indicate when PLAYLIST NAME IS ACTUALLY MATCHED
#?? NO printed *** notifications----------------------
#?? made print_to_screen write to log if DEBUG to log is enabled
#?? configurable debug to write to screen/log/none
#?? PR - flag file delete at start
#?? PR - wrong comment (-l) reference
#?? use generic routine of send_notification instead of send_sms
#?? matching playlist means instant detection (and optional notify) rather than counting
#?? don't show 'icon' if in the exception process
#?? error checking for keys 'icon', 'url', 'refresh', 'notify', and 'override'
#?? playlist exception should only apply if actually in a playlist versus building up the count
#?? DEBUG: SONG CHANGE -> print song because it's hard to keep track in log
#?? printing weird -> ICON_SONG_MISSING_FROM_PLAYLIST character spacing weird
#?? if song in two playlists, attribute it the active one first
#?? playlist url sometimes blank
#?? fix case of double-counting song
#?? emails/texts missing -> f"*** {notify_playlist['name']} Detected: {songstr}, Song Count: {notify_playlist['count_start']}" [notify was off for Liked Songs]
#?? fixed COUNT START: 0 next song after an exception granted
#?? Added playlist name to DEBUG: debug statements around finding playlist or not hitting exception limit
#?? Add DEBUG: COUNT_END debug info when playlist not found
#?? When handling exceptions to monitored playlists, need to reset it all back as if it was OK (ex: is_playlist = True)6
#?? When restarting on detected playlist, missing playlist assignment, context: album, and icon appending
#?? No *** detected on screen sometimes
#?? errant 'override' always at user becoming active later (not at restart)
#?? remove spaces before/after playlist and song names
#?? what -> Prints the list of Spotify friends with the last listened track (-l flag)
#?? JMK showing up at end of URLs?
#?? periodic tracks stop if frequency is 0
#?? playlist compare periodically checks entire playlist set and not just length (# of songs)
#?? when printing "monitoring tracks" should I should subdetail (alert? icons?)
#?? wrong playlist (white noise) in email and log
#?? playlist URL blank - add a key?
#?? configurable icon if song not found in playlist
#?? added alert key for each monitored playlist (PLAYLIST_NOTIFICATION equivalent)
#?? initial active jmk email and original emails missing count and playlist (it's hit or miss) - See 2:30pm 7/21
#?? JMK_MODE only to override start count if playlist already in action
#?? playlist detected notes not being shown on screen
#++ does count ever go above 3?
#++ initial active original email missing
#++ initial active getting 3rd text with count info
#++ restored original MONITOR_LIST_FILE functionality

#!/usr/bin/env python3
"""
Author: Michal Szymanski <misiektoja-github@rm-rf.ninja>
v2.9.2

Tool implementing real-time tracking of Spotify friends music activity:
https://github.com/misiektoja/spotify_monitor/

Python pip3 requirements:

requests
python-dateutil
urllib3
pyotp (optional, needed when the token source is set to cookie)
python-dotenv (optional)
wcwidth (optional, needed by TRUNCATE_CHARS feature)
spotipy (required since v2.7 due to new Spotify restrictions introduced on 22 Dec 2025)
"""

VERSION = "2.9.2"

# API 401 error means sp_dc cookie has expired. Lasts one year. 03/15/2025

# spotify-friend-stalker: https://github.com/moritzlauper/spotify-friend-stalker (node.js)
# spotify-buddylist API:  https://github.com/valeriangalliat/spotify-buddylist (node.js)
# spotify-api:            https://developer.spotify.com/documentation/web-api (official API)
# spotify-monitor:        https://github.com/misiektoja/spotify_monitor/
# spotify-api-python:     https://github.com/thlucas1/SpotifyWebApiPython (reference only)

# revision history
# 2025/03/28: Finished porting "spotify logger" features of JMK into this app (python, and maintained)
# 2025/03/29: Changed timeout for user playing stopped from 11 mins to 'song length + SPOTIFY_INACTIVITY_CHECK_MARGIN' to match "spotify logger"
# 2025/03/29: Reload any monitored playlists from file every hour
# 2025/03/29: Restored original timeout mechanism (can't use song + margin because song is the last-song-played not the current song)
# 2025/03/29: Added exponentional backoff on retries (**)
# 2025/03/29: Errors are put into log file and not on screen (ex: searchPlaylist error)
# 2025/03/30: Lots of little bug and operational fixes for Discovery Zone
# 2025/03/30: Updated to 1.8.2 from spotify_monitor source
# 2025/03/31: Fixed duplicative DZ logic causing 2 hearts.
# 2025/03/31: Moved remnant calls to _upper logic instead of map() logic
# 2025/03/31: Use songstring() in all instances of send_email
# 2025/03/31: Use upper() on compares in search_playlist
# 2025/03/31: Only check if 'Liked Songs' if NOT 'Discovery Zone'fs
# 2025/04/01: Lots of DZ bug fixes
# 2025/04/01: Periodic load file was loading the same playlist twice instead of different ones
# 2025/04/01: Added notice of duplicate songs removed during periodic load
# 2025/04/01: Combined two periodic load functions into one via ChatGPT
# 2025/04/01: Put midstream Discover Zone detected/cleared messages after song name printed on screen
# 2025/04/04: Added SMS message text to the SMS events in log
# 2025/04/04: Send discovery zone detected SMS after the START SMS
# 2025/04/04: Fix incorrect log info where 'not found in playlist' message was after overriding to 'unknown'
# 2025/04/04: Don't send duplicate emails for song changes (original spotify_monitor emails & JMK_MODE emails)
# 2025/04/04: Updated spotify_profile_monitor to avoid this due to spotify fetch error: *** Load Tracks: Fri Apr  4 06:20:35 2025, 1 songs [was: 302] in dz_songs.txt [0 duplicates removed]
# 2025/04/06: Don't overwrite valid existing playlist name to [liked songs]
# 2025/04/11: Remove 2nd space between timestamp and song names in JMK_MODE emails
# 2025/04/16: Add a \n in DZ message before "DZ Count & DZ Playlist" to put those on another line
# 2025/04/16: Strip \n from text messages in send_sms
# 2025/04/16: Change formatting of the SUCCESS and ERROR logged events in send_sms
# 2025/04/16: Don't put 2nd DZ MSG after a user goes inactive
# 2025/04/22: WIP: Allow a 1 song exception before exiting Discovery Zone
# 2025/04/28: Added option to truncate output to avoid line wrapping
# 2025/06/10: Migrated to latest code base
# 2025/06/10: Modified look & feel of configuration flags logging at startup
# 2025/06/10: Show stats on monitored playlists (discovery zone & liked songs) on screen during initial startup
# 2025/06/21: Line truncation feature value of 999 now does autodetection of screen width
# 2025/06/21: Don't show songs played on first boot when active
# 2025/06/25: Removed redundant variables for tracks_upper (used) and sp_tracks (unused)
# 2025/06/25: Removed song_count variable, since it's already there (listened_songs)
# 2025/06/28: Show elapsed-session-time after "Songs Played:" on each email update
# 2025/06/28: Fixed truncation by treating tabs as spaces. Removed subtracting two from screen width during truncation auto-calculation
# 2025/06/29: Optional flag file to indicate streaming state to other apps
# 2025/06/29: Fix first email not going out for [00] song when user becomes active in JMK_MODE
# 2025/07/02: Pull in latest source changes
# 2025/07/02: Fix message truncation if message is multiple lines via \n
# 2025/07/02: Fix DZ Cleared message when going from DZ Playlist to not DZ Playlist
# 2025/07/03: Added support for setting the FLAG_FILE_PATH
# 2025/07/03: Fixed crashing when logging was disabled
# 2025/07/03: Submitted PR: Missing *
# 2025/07/03: Submitted PR: Song Counts & Time Elapsed
# 2025/07/03: Submitted PR: Line truncation
# 2025/07/03: Submitted PR: Flag file
# 2025/07/07: Fixed truncation to support multi-character-width emojis
# 2025/07/13: Simplified start-text-sent and end-text-sent on-screen messaging
# 2025/07/18: When song not found in playlist, leave the playlist name but indicate with a 'warning' emoji
# 2025/07/20: Completely redid code for DZ and Liked Songs to make it generic for a PR, and more flexible, and to support hysteresis for smart shuffle
# 2025/10/04: If "unknown playlist", don't send that on NTYF alert
# 2025/10/05: NTFY now skips image processing if image_url = ""
# 2025/10/05: Adjusted BE-HUMAN logic to consider # of hours actually monitoring out of 24
# 2025/10/17: Honor tags for send_ntfy topic2 to better differentiate start/stops within stream
# 2025/10/25: Use one NTFY topic for all updates. Use NTFY library code
# 2025/10/25: New priority scheme for send_NTFY (and lower JMK to 1's)
# 2025/10/25: Fix images broken on 10/05/2025 change. Added NTFY_IMAGES as a configuration
# 2025/11/01: New priority scheme for send_ntfy. KEL stopping is now low, only start is high
# 2025/12/27: New spotify API scheme required
# 2025/12/27: New playlist image method required due to spotify API change for spotify-owned editorial playlists
# 2025/12/28: Updated to latest code base
# 2025/01/18: Added missing (custom) to END notifications of playlists
# 2025/01/18: Removed Twilio and send_sms support. Current mechanism is NTFY
# 2025/01/18: Fixed JMK_MODE emails not being sent for stream except START/initial song. Broke after updating code base on 12/25/25
# 2025/02/19: Fixed duplicate emails introduced with catching up to latest code base
# 2025/02/19: Fixed duplicate listened_songs += 1 introduced with catching up to latest code base
# 2025/02/22: Fixed exception crash if error (but not 404) occurs during fetching playlist image URL
# 2025/02/27: Fixed exception crash if error (but not 404) occurs during spotify_get_playlist_owner
# 2025/02/28: Fixed missing 'discovery zone cleared' messages
# 2025/03/14: Check DEBUG_JMK within print_debug, eliminating all those IF statements. Rename JMK_DEBUG to DEBUG_JMK
# 2025/03/14: Rename 'texts' to 'notify'
# 2025/04/19: Fixed errant blank line
# 2025/07/12: Added code to update google sheet directly (via Claude)
# 2025/07/13: Removed configcat
# 2025/07/13: Added printing of JMK added items in configuration items at startup`

# bugs and to-dos:
# start/end texts include DZ count if > 0?
# *** PR: identify playlists via song lists and auto-refresh
# *** PR: NTFY (a free notification service would be better)
# profile monitor: * Error, retrying in 5 minutes: fetch_server_time() head network request error: HTTPSConnectionPool(host='open.spotify.com', port=443): Read timed out. (read timeout=15)
# *** alternate notification method (pushover, gotify, ntfy.sh )
# *** give discovery zone a +1 song grace after DZ identified [but how to message this, etc] -> started the work, see DZexceptions
# ***      detect smart shuffle songs, for JMK at least??
# *** why not write straight to the gdrive spreadsheet instead of indirectly via email?

# command line examples
# *** see .conf file

# ---------------------------
# CONFIGURATION SECTION START
# ---------------------------

CONFIG_BLOCK = """
# Select the method used to obtain the Spotify access token
# Available options:
#   cookie - uses the sp_dc cookie to retrieve a token via the Spotify web endpoint (recommended)
#   client - uses captured credentials from the Spotify desktop client and a Protobuf-based login flow (for advanced users)
TOKEN_SOURCE = "cookie"

# ---------------------------------------------------------------------

# The section below is used when the token source is set to 'cookie'
# (to configure the alternative 'client' method, see the section at the end of this config block)
#
# - Log in to Spotify web client (https://open.spotify.com/) and retrieve your sp_dc cookie
#   (use your web browser's dev console or "Cookie-Editor" by cgagnier to extract it easily: https://cookie-editor.com/)
# - Provide the SP_DC_COOKIE secret using one of the following methods:
#   - Pass it at runtime with -u / --spotify-dc-cookie
#   - Set it as an environment variable (e.g. export SP_DC_COOKIE=...)
#   - Add it to ".env" file (SP_DC_COOKIE=...) for persistent use
#   - Fallback: hard-code it in the code or config file
SP_DC_COOKIE = "your_sp_dc_cookie_value"

# ---------------------------------------------------------------------

# The section below is used to get tracks and user info via secondary token (Client Credentials OAuth Flow - 'oauth_app')
#
# To obtain the credentials:
#   - Log in to Spotify Developer dashboard: https://developer.spotify.com/dashboard
#   - Create a new app
#   - For 'Redirect URL', use: http://127.0.0.1:1234
#   - Select 'Web API' as the intended API
#   - Copy the 'Client ID' and 'Client Secret'
#
# Provide the SP_APP_CLIENT_ID and SP_APP_CLIENT_SECRET secrets using one of the following methods:
#   - Pass it at runtime with -r / --oauth-app-creds (use SP_APP_CLIENT_ID:SP_APP_CLIENT_SECRET format - note the colon separator)
#   - Set it as an environment variable (e.g. export SP_APP_CLIENT_ID=...; export SP_APP_CLIENT_SECRET=...)
#   - Add it to ".env" file (SP_APP_CLIENT_ID=... and SP_APP_CLIENT_SECRET=...) for persistent use
#   - Fallback: hard-code it in the code or config file
#
# The tool automatically refreshes the access token, so it remains valid indefinitely
SP_APP_CLIENT_ID = "your_spotify_app_client_id"
SP_APP_CLIENT_SECRET = "your_spotify_app_client_secret"

# Path to cache file used to store OAuth app access tokens across tool restarts
# Set to empty to use in-memory cache only
SP_APP_TOKENS_FILE = ".spotify-monitor-oauth-app.json"

# ---------------------------------------------------------------------

# SMTP settings for sending email notifications
# If left as-is, no notifications will be sent
#
# Provide the SMTP_PASSWORD secret using one of the following methods:
#   - Set it as an environment variable (e.g. export SMTP_PASSWORD=...)
#   - Add it to ".env" file (SMTP_PASSWORD=...) for persistent use
# Fallback:
#   - Hard-code it in the code or config file
SMTP_HOST = "your_smtp_server_ssl"
SMTP_PORT = 587
SMTP_USER = "your_smtp_user"
SMTP_PASSWORD = "your_smtp_password"
SMTP_SSL = True
SENDER_EMAIL = "your_sender_email"
RECEIVER_EMAIL = "your_receiver_email"

# Whether to send an email when user becomes active
# Can also be enabled via the -a flag
ACTIVE_NOTIFICATION = False

# Whether to send an email when user goes inactive
# Can also be enabled via the -i flag
INACTIVE_NOTIFICATION = False

# Whether to send an email when a monitored track/playlist/album plays
# Can also be enabled via the -t flag
TRACK_NOTIFICATION = False

# Whether to send an email on every song change
# Can also be enabled via the -j flag
SONG_NOTIFICATION = False

# Whether to send an email when user plays a song on loop
# Triggered if the same song is played more than SONG_ON_LOOP_VALUE times
# Can also be enabled via the -x flag
SONG_ON_LOOP_NOTIFICATION = False

# Whether to send an email on errors
# Can also be disabled via the -e flag
ERROR_NOTIFICATION = True

# How often to check for user activity; in seconds
# Can also be set using the -c flag
SPOTIFY_CHECK_INTERVAL = 30  # 30 seconds

# Time to wait before retrying after an error; in seconds
SPOTIFY_ERROR_INTERVAL = 180  # 3 mins

# Time after which a user is considered inactive (based on last activity); in seconds
# Can also be set using the -o flag
# Note: If the user listens to songs longer than this value, they may be marked as inactive
SPOTIFY_INACTIVITY_CHECK = 660  # 11 mins

# How many recently listened songs to display in the inactive notification email
# Set to 0 to disable the recently listened songs list
INACTIVE_EMAIL_RECENT_SONGS_COUNT = 5

# Tolerance in seconds for "Played for" display when comparing actual playback time to track duration
# If the difference is within +-PLAYED_FOR_DURATION_TOLERANCE seconds, "Played for" is suppressed
# (treats as if song was played for its full duration to account for timestamp jitter)
PLAYED_FOR_DURATION_TOLERANCE = 1

# Whether to detect and annotate crossfaded songs (songs played with transition timing)
# When enabled, songs played within the crossfade detection thresholds will be marked as
# "(X% - crossfade enabled)" to indicate that the song likely ended early due to crossfade transitions
DETECT_CROSSFADED_SONGS = True

# Thresholds for crossfade detection (as percentage of track duration)
# Songs played between CROSSFADE_DETECTION_MIN and CROSSFADE_DETECTION_MAX will be annotated
# as crossfaded if DETECT_CROSSFADED_SONGS is enabled
CROSSFADE_DETECTION_MIN = 0.96  # 96% - minimum percentage to consider crossfade
CROSSFADE_DETECTION_MAX = 0.99  # 99% - maximum percentage to consider crossfade

# Interval for checking if a user who disappeared from the list of recently active friends has reappeared; in seconds
# Can happen due to:
#   - unfollowing the user
#   - Spotify service issues
#   - private session bugs
#   - user inactivity for over a week
# In such a case, the tool will continuously check for the user's reappearance using the time interval specified below
# Can also be set using the -m flag
SPOTIFY_DISAPPEARED_CHECK_INTERVAL = 180  # 3 mins

# Whether to auto-play each listened song in your Spotify client
# Can also be set using the -g flag
TRACK_SONGS = False

# Method used to play the song listened by the tracked user in local Spotify client under macOS
# (i.e. when TRACK_SONGS / -g functionality is enabled)
# Methods:
#       "apple-script" (recommended)
#       "trigger-url"
SPOTIFY_MACOS_PLAYING_METHOD = "apple-script"

# Method used to play the song listened by the tracked user in local Spotify client under Linux OS
# (i.e. when TRACK_SONGS / -g functionality is enabled)
# Methods:
#       "dbus-send" (most common one)
#       "qdbus"
#       "trigger-url"
SPOTIFY_LINUX_PLAYING_METHOD = "dbus-send"

# Method used to play the song listened by the tracked user in local Spotify client under Windows OS
# (if TRACK_SONGS / -g functionality is enabled)
# Methods:
#       "start-uri" (recommended)
#       "spotify-cmd"
#       "trigger-url"
SPOTIFY_WINDOWS_PLAYING_METHOD = "start-uri"

# Number of consecutive plays of the same song considered to be on loop
SONG_ON_LOOP_VALUE = 3

# Threshold for considering a song as skipped (fraction of duration)
SKIPPED_SONG_THRESHOLD = 0.55  # song is treated as skipped if played for <= 55% of its total length

# Spotify track ID to play when the user goes offline (used when TRACK_SONGS / -g functionality is enabled)
# Leave empty to simply pause
# SP_USER_GOT_OFFLINE_TRACK_ID = "5wCjNjnugSUqGDBrmQhn0e"
SP_USER_GOT_OFFLINE_TRACK_ID = ""

# Delay before pausing the above track after the user goes offline; in seconds
# Set to 0 to keep playing indefinitely until manually paused
SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE = 5  # 5 seconds

# Occasionally, the Spotify API glitches and reports that the user has disappeared from the list of friends
# To avoid false alarms, we delay alerts until this happens REMOVED_DISAPPEARED_COUNTER times in a row
REMOVED_DISAPPEARED_COUNTER = 4

# Optional: specify user agent manually
#
# When the token source is 'cookie' - set it to web browser user agent, some examples:
# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
#
# When the token source is 'client' - set it to Spotify desktop client user agent, some examples:
# Spotify/126200580 Win32_x86_64/0 (PC desktop)
# Spotify/126400408 OSX_ARM64/OS X 15.5.0 [arm 2]
#
# Leave empty to auto-generate it randomly for specific token source
USER_AGENT = ""

# How often to print a "liveness check" message to the output; in seconds
# Set to 0 to disable
LIVENESS_CHECK_INTERVAL = 43200  # 12 hours

# URL used to verify internet connectivity at startup
CHECK_INTERNET_URL = 'https://api.spotify.com/v1'

# Timeout used when checking initial internet connectivity; in seconds
CHECK_INTERNET_TIMEOUT = 5

# Whether to enable / disable SSL certificate verification while sending https requests
VERIFY_SSL = True

# Threshold for displaying Spotify 50x errors - it is to suppress sporadic issues with Spotify API endpoint
# Adjust the values according to the SPOTIFY_CHECK_INTERVAL timer
# If more than 6 Spotify API related errors in 4 minutes, show an alert
ERROR_500_NUMBER_LIMIT = 6
ERROR_500_TIME_LIMIT = 240  # 4 min

# Threshold for displaying network errors - it is to suppress sporadic issues with internet connectivity
# Adjust the values according to the SPOTIFY_CHECK_INTERVAL timer
# If more than 6 network related errors in 4 minutes, show an alert
ERROR_NETWORK_ISSUES_NUMBER_LIMIT = 6
ERROR_NETWORK_ISSUES_TIME_LIMIT = 240  # 4 min

# CSV file to write every listened track
# Can also be set using the -b flag
CSV_FILE = ""

# Filename with Spotify tracks/playlists/albums to alert on
# Can also be set using the -s flag
MONITOR_LIST_FILE = ""

# Location of the optional dotenv file which can keep secrets
# If not specified it will try to auto-search for .env files
# To disable auto-search, set this to the literal string "none"
# Can also be set using the --env-file flag
DOTENV_FILE = ""

# Suffix to append to the output filenames instead of default user URI ID
# Can also be set using the -y flag
FILE_SUFFIX = ""

# Base name for the log file. Output will be saved to spotify_monitor_<user_uri_id/file_suffix>.log
# Can include a directory path to specify the location, e.g. ~/some_dir/spotify_monitor
SP_LOGFILE = "spotify_monitor"

# Whether to disable logging to spotify_monitor_<user_uri_id/file_suffix>.log
# Can also be disabled via the -d flag
DISABLE_LOGGING = False

# Enable debug mode for technical logging (can also be enabled via --debug flag)
# Shows request flow, selected params and internal state changes (with sensitive values redacted)
DEBUG_MODE = False

# Width of horizontal line
HORIZONTAL_LINE = 113

# Whether to clear the terminal screen after starting the tool
CLEAR_SCREEN = True

# Path to a file that is created when the user is active and deleted when inactive
# Useful for external tools to detect streaming status
# Can also be set via the --flag-file flag
FLAG_FILE = ""

# Max characters per line when printing to screen to avoid line wrapping
# Does not affect log file output
# Set to 999 to auto-detect terminal width
# Applies only when DISABLE_LOGGING is False
# Can also be set via the --truncate flag
TRUNCATE_CHARS = 0

# Value added/subtracted via signal handlers to adjust inactivity timeout (SPOTIFY_INACTIVITY_CHECK); in seconds
SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE = 30  # 30 seconds

# Whether to show Apple Music URL in console and emails
ENABLE_APPLE_MUSIC_URL = True

# Whether to show YouTube Music URL in console and emails
ENABLE_YOUTUBE_MUSIC_URL = True

# Whether to show Amazon Music URL in console and emails
ENABLE_AMAZON_MUSIC_URL = False

# Whether to show Deezer URL in console and emails
ENABLE_DEEZER_URL = False

# Whether to show Tidal URL in console and emails
# Note: Tidal requires users to be logged in to their account in the web browser to use the search functionality
ENABLE_TIDAL_URL = False

# Whether to show Genius lyrics URL in console and emails
ENABLE_GENIUS_LYRICS_URL = True

# Whether to show AZLyrics URL in console and emails
ENABLE_AZLYRICS_URL = False

# Whether to show Tekstowo.pl lyrics URL in console and emails
ENABLE_TEKSTOWO_URL = False

# Whether to show Musixmatch lyrics URL in console and emails
# Note: Musixmatch requires users to be logged in to their account in the web browser to use the search functionality
ENABLE_MUSIXMATCH_URL = False

# Whether to show Lyrics.com lyrics URL in console and emails
ENABLE_LYRICS_COM_URL = False

# String to add after playlist name to indicate it's a Spotify public curated and customized playlist
# The distinction may be important because the songs will vary by account due to listening habits.
# This will be used for messages on console and emails
# The string should include all desired characters, including a preceding space and parenthesis, if desired
#
# Example:
#   For: 90s Pop (by Spotify), SPOTIFY_SUFFIX = " (by Spotify)"
#
# Leave empty to disable
SPOTIFY_SUFFIX = ""

# The Spotify API sometimes doesn't provide specific public shared playlists for a user.
# This allows you to add one or more playlists to be monitored
#
# Replace {playlist_id} with the ID of the playlist to monitor, and replace {user_id} with the ID for the owner of the playlist
#
# ADD_PLAYLISTS_TO_MONITOR = [
#   {'uri': 'spotify:playlist:{playlist_id}', 'owner_name': '{user_id}', 'owner_uri': 'spotify:user:{user_id}'},
#   {'uri': 'spotify:playlist:{playlist_id}', 'owner_name': '{user_id}', 'owner_uri': 'spotify:user:{user_id}'}
# ]
#
# example: [ {'uri': 'spotify:playlist:6pYPhRkJMSg1d7j8RHgJK1', 'owner_name': 'teocida', 'owner_uri': 'spotify:user:teocida'} ]
# example: [ {'uri': 'spotify:playlist:0AyBQ5uEhJgdh2NFcMe6wb', 'owner_name': 'uwacwfv5hr23atg1v3dez1sxs', 'owner_uri': 'spotify:user:uwacwfv5hr23atg1v3dez1sxs'} ]
#

LOAD_TRACKS_FREQUENCY = 3600 # 1 hour
ADD_PLAYLISTS_TO_MONITOR = []

# ---------------------------------------------------------------------

# The section below is used when the token source is set to 'cookie'

# Maximum number of attempts to get a valid access token in a single run of the spotify_get_access_token_from_sp_dc() function
TOKEN_MAX_RETRIES = 3

# Interval between access token retry attempts; in seconds
TOKEN_RETRY_TIMEOUT = 0.5  # 0.5 second

# Mapping of TOTP version identifiers to the secrets needed for TOTP generation
# Newest secrets are downloaded automatically from SECRET_CIPHER_DICT_URL (see below)
# Can also be fetched via spotify_monitor_secret_grabber.py utility - see debug dir
SECRET_CIPHER_DICT = {
    "61": [44, 55, 47, 42, 70, 40, 34, 114, 76, 74, 50, 111, 120, 97, 75, 76, 94, 102, 43, 69, 49, 120, 118, 80, 64, 78],
}

# Remote or local URL used to fetch updated secrets needed for TOTP generation
# Set to empty string to disable
# If you used "spotify_monitor_secret_grabber.py --secretdict > secretDict.json" specify the file location below
SECRET_CIPHER_DICT_URL = "https://raw.githubusercontent.com/xyloflake/spot-secrets-go/main/secrets/secretDict.json"
# SECRET_CIPHER_DICT_URL = file:///C:/your_path/secretDict.json
# SECRET_CIPHER_DICT_URL = "file:///your_path/secretDict.json"

# Identifier used to select the appropriate secret from SECRET_CIPHER_DICT when generating a TOTP token
# Set to 0 to auto-select the highest available version
TOTP_VER = 0

# ---------------------------------------------------------------------

# The section below is used when the token source is set to 'client'
#
# - Run an intercepting proxy of your choice (like Proxyman)
# - Launch the Spotify desktop client and look for requests to: https://login{n}.spotify.com/v3/login
#   (the 'login' part is suffixed with one or more digits)
# - Export the login request body (a binary Protobuf payload) to a file
#   (e.g. in Proxyman: right click the request -> Export -> Request Body -> Save File -> <login-request-body-file>)
#
# To automatically extract DEVICE_ID, SYSTEM_ID, USER_URI_ID and REFRESH_TOKEN from the exported binary login
# request Protobuf file:
#
# - Run the tool with the -w flag to indicate an exported file or specify its file name below
LOGIN_REQUEST_BODY_FILE = ""

# Alternatively, you can manually set the DEVICE_ID, SYSTEM_ID, USER_URI_ID and REFRESH_TOKEN options
# (however, using the automated method described above is recommended)
#
# These values can be extracted using one of the following methods:
#
# - Run spotify_profile_monitor with the -w flag without specifying SPOTIFY_USER_URI_ID - it will decode the file and
#   print the values to stdout, example:
#       spotify_profile_monitor --token-source client -w <path-to-login-request-body-file>
#
# - Use the protoc tool (part of protobuf pip package):
#       pip install protobuf
#       protoc --decode_raw < <path-to-login-request-body-file>
#
# - Use the built-in Protobuf decoder in your intercepting proxy (if supported)
#
# The Protobuf structure is as follows:
#
#    {
#      1: {
#           1: "DEVICE_ID",
#           2: "SYSTEM_ID"
#         },
#      100: {
#           1: "USER_URI_ID",
#           2: "REFRESH_TOKEN"
#         }
#    }
#
# Provide the extracted values below (DEVICE_ID, SYSTEM_ID, USER_URI_ID). The REFRESH_TOKEN secret can be
# supplied using one of the following methods:
#   - Set it as an environment variable (e.g. export REFRESH_TOKEN=...)
#   - Add it to ".env" file (REFRESH_TOKEN=...) for persistent use
#   - Fallback: hard-code it in the code or config file
DEVICE_ID = "your_spotify_app_device_id"
SYSTEM_ID = "your_spotify_app_system_id"
USER_URI_ID = "your_spotify_user_uri_id"
REFRESH_TOKEN = "your_spotify_app_refresh_token"

# ----------------------------------------------
# Advanced options for 'client' token source
# Modifying the values below is NOT recommended!
# ----------------------------------------------

# Spotify login URL
LOGIN_URL = "https://login5.spotify.com/v3/login"

# Spotify client token URL
CLIENTTOKEN_URL = "https://clienttoken.spotify.com/v1/clienttoken"

# Platform-specific values for token generation so the Spotify client token requests match your exact Spotify desktop
# client build (arch, OS build, app version etc.)
#
# - Run an intercepting proxy of your choice (like Proxyman)
# - Launch the Spotify desktop client and look for requests to: https://clienttoken.spotify.com/v1/clienttoken
#   (these requests are sent every time client token expires, usually every 2 weeks)
# - Export the client token request body (a binary Protobuf payload) to a file
#   (e.g. in Proxyman: right click the request -> Export -> Request Body -> Save File -> <clienttoken-request-body-file>)
#
# To automatically extract APP_VERSION, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR and CLIENT_MODEL from the
# exported binary client token request Protobuf file:
#
# - Run the tool with the hidden -z flag to indicate an exported file or specify its file name below
CLIENTTOKEN_REQUEST_BODY_FILE = ""

# Alternatively, you can manually set the APP_VERSION, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR and
# CLIENT_MODEL options
#
# These values can be extracted using one of the following methods:
#
# - run spotify_profile_monitor with the hidden -z flag without specifying SPOTIFY_USER_URI_ID - it will decode the file
#   and print the values to stdout, example:
#       spotify_profile_monitor --token-source client -z <path-to-clienttoken-request-body-file>
#
# - use the protoc tool (part of protobuf pip package):
#       pip install protobuf
#       protoc --decode_raw < <path-to-clienttoken-request-body-file>
#
# - use the built-in Protobuf decoder in your intercepting proxy (if supported)
#
# The Protobuf structure is as follows:
#
# 1: 1
# 2 {
#   1: "APP_VERSION"
#   2: "DEVICE_ID"
#   3 {
#     1 {
#       4 {
#         1: "CPU_ARCH"
#         3: "OS_BUILD"
#         4: "PLATFORM"
#         5: "OS_MAJOR"
#         6: "OS_MINOR"
#         8: "CLIENT_MODEL"
#       }
#     }
#     2: "SYSTEM_ID"
#   }
# }
#
# Provide the extracted values below (except for DEVICE_ID and SYSTEM_ID as it was already provided via -w)
CPU_ARCH = 10
OS_BUILD = 19045
PLATFORM = 2
OS_MAJOR = 9
OS_MINOR = 9
CLIENT_MODEL = 34404

# App version (e.g. '1.2.62.580.g7e3d9a4f')
# Leave empty to auto-generate from USER_AGENT
APP_VERSION = ""

"""

# -------------------------
# CONFIGURATION SECTION END
# -------------------------

# Default dummy values so linters shut up
# Do not change values below - modify them in the configuration section or config file instead
TOKEN_SOURCE = ""
SP_DC_COOKIE = ""
SP_APP_CLIENT_ID = ""
SP_APP_CLIENT_SECRET = ""
SP_APP_TOKENS_FILE = ""
LOGIN_REQUEST_BODY_FILE = ""
CLIENTTOKEN_REQUEST_BODY_FILE = ""
LOGIN_URL = ""
DEVICE_ID = ""
SYSTEM_ID = ""
USER_URI_ID = ""
REFRESH_TOKEN = ""
CLIENTTOKEN_URL = ""
APP_VERSION = ""
CPU_ARCH = 0
OS_BUILD = 0
PLATFORM = 0
OS_MAJOR = 0
OS_MINOR = 0
CLIENT_MODEL = 0
SMTP_HOST = ""
SMTP_PORT = 0
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_SSL = False
SENDER_EMAIL = ""
RECEIVER_EMAIL = ""
ACTIVE_NOTIFICATION = False
INACTIVE_NOTIFICATION = False
TRACK_NOTIFICATION = False
SONG_NOTIFICATION = False
SONG_ON_LOOP_NOTIFICATION = False
ERROR_NOTIFICATION = False
SPOTIFY_CHECK_INTERVAL = 0
SPOTIFY_ERROR_INTERVAL = 0
SPOTIFY_INACTIVITY_CHECK = 0
INACTIVE_EMAIL_RECENT_SONGS_COUNT = 0
PLAYED_FOR_DURATION_TOLERANCE = 0
DETECT_CROSSFADED_SONGS = False
CROSSFADE_DETECTION_MIN = 0.0
CROSSFADE_DETECTION_MAX = 0.0
SPOTIFY_DISAPPEARED_CHECK_INTERVAL = 0
TRACK_SONGS = False
SPOTIFY_MACOS_PLAYING_METHOD = ""
SPOTIFY_LINUX_PLAYING_METHOD = ""
SPOTIFY_WINDOWS_PLAYING_METHOD = ""
SONG_ON_LOOP_VALUE = 0
SKIPPED_SONG_THRESHOLD = 0
SP_USER_GOT_OFFLINE_TRACK_ID = ""
SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE = 0
REMOVED_DISAPPEARED_COUNTER = 0
USER_AGENT = ""
LIVENESS_CHECK_INTERVAL = 0
CHECK_INTERNET_URL = ""
CHECK_INTERNET_TIMEOUT = 0
VERIFY_SSL = False
ERROR_500_NUMBER_LIMIT = 0
ERROR_500_TIME_LIMIT = 0
ERROR_NETWORK_ISSUES_NUMBER_LIMIT = 0
ERROR_NETWORK_ISSUES_TIME_LIMIT = 0
CSV_FILE = ""
MONITOR_LIST_FILE = ""
DOTENV_FILE = ""
FILE_SUFFIX = ""
SP_LOGFILE = ""
DISABLE_LOGGING = False
DEBUG_MODE = False
HORIZONTAL_LINE = 0
CLEAR_SCREEN = False
SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE = 0
ENABLE_GENIUS_LYRICS_URL = False
ENABLE_AZLYRICS_URL = False
ENABLE_TEKSTOWO_URL = False
ENABLE_MUSIXMATCH_URL = False
ENABLE_LYRICS_COM_URL = False
ENABLE_APPLE_MUSIC_URL = False
ENABLE_YOUTUBE_MUSIC_URL = False
ENABLE_AMAZON_MUSIC_URL = False
ENABLE_DEEZER_URL = False
ENABLE_TIDAL_URL = False
TOKEN_MAX_RETRIES = 0
TOKEN_RETRY_TIMEOUT = 0.0
SECRET_CIPHER_DICT = {}
SECRET_CIPHER_DICT_URL = ""
TOTP_VER = 0
FLAG_FILE = ""
TRUNCATE_CHARS = 0
SPOTIFY_SUFFIX = ""

JMK_MODE = False
ALT_VIEW = False
ALT_COOKIE = False
DISCOVERY_ZONE_FOUND_COUNT = 3
DISCOVERY_ZONE_EXCEPTIONS_ALLOWED = 1
UPDATE_SPREADSHEET = False
SPREADSHEET_ID = ""
GOOGLE_OAUTH_CLIENT_FILE = ""
GOOGLE_OAUTH_TOKEN_FILE = ""
#DZ_PLAYLIST_NAME = "Discovery Zone"
#LIKED_PLAYLIST_NAME = "Liked Songs"
INITIAL_STARTUP = True
#sp_tracks  = []
#sp_tracks2 = []
# sp_tracks_upper  = [] # Discovery Zone
# sp_tracks2_upper = [] # Liked Songs
USER_ID       = ""
GMAIL_TAG     = ""
ERR_CODE      = ""
SEND_NOTIFY   = False
DZ_ALERTS     = False
ORIG_EMAILS   = False
SP_DC_COOKIE2 = ""
LOGIN_REQUEST_BODY_FILE2 = ""
LOAD_TRACKS_FREQUENCY = 3600 # 1 hour
monitored_playlists_data = {}
DEBUG_JMK = False
count_overridden = False
NTFY_IMAGES = True

# NTFY configuration
NTFY_TOPIC_KEL = "jeoff_spotify_stream"
NTFY_TOPIC_JMK = "jeoff_spotify_stream_jmk"

from datetime import timezone
import threading

import logging
from io import StringIO, BytesIO
from PIL import Image

exec(CONFIG_BLOCK, globals())

# Default name for the optional config file
DEFAULT_CONFIG_FILENAME = "spotify_monitor.conf"

# List of secret keys to load from env/config
SECRET_KEYS = ("REFRESH_TOKEN", "SP_DC_COOKIE", "SMTP_PASSWORD", "SP_APP_CLIENT_ID", "SP_APP_CLIENT_SECRET")
SECRET_KEYS+= ("SP_DC_COOKIE2", ) # comma needed to make this a tuple, otherwise error

# Strings removed from track names for generating proper Genius search URLs
re_search_str = r'remaster|extended|original mix|remix|original soundtrack|radio( |-)edit|\(feat\.|( \(.*version\))|( - .*version)'
re_replace_str = r'( - (\d*)( )*remaster$)|( - (\d*)( )*remastered( version)*( \d*)*.*$)|( \((\d*)( )*remaster\)$)|( - (\d+) - remaster$)|( - extended$)|( - extended mix$)|( - (.*); extended mix$)|( - extended version$)|( - (.*) remix$)|( - remix$)|( - remixed by .*$)|( - original mix$)|( - .*original soundtrack$)|( - .*radio( |-)edit$)|( \(feat\. .*\)$)|( \(\d+.*Remaster.*\)$)|( \(.*Version\))|( - .*version)'

# Default value for network-related timeouts in functions; in seconds
FUNCTION_TIMEOUT = 15

# Default value for alarm signal handler timeout; in seconds
ALARM_TIMEOUT = 15
ALARM_RETRY = 10

# Variables for caching functionality of the Spotify 'cookie' access token and 'client' refresh token to avoid unnecessary refreshing
SP_CACHED_ACCESS_TOKEN = None
SP_CACHED_REFRESH_TOKEN = None
SP_ACCESS_TOKEN_EXPIRES_AT = 0
SP_CACHED_CLIENT_ID = ""

# Variables for caching OAuth app access token (Client Credentials Flow)
SP_CACHED_OAUTH_APP_TOKEN = None

# URL of the Spotify Web Player endpoint to get access token
TOKEN_URL = "https://open.spotify.com/api/token"

# URL of the endpoint to get server time needed to create TOTP object
SERVER_TIME_URL = "https://open.spotify.com/"

# Variables for caching functionality of the Spotify client token to avoid unnecessary refreshing
SP_CACHED_CLIENT_TOKEN = None
SP_CLIENT_TOKEN_EXPIRES_AT = 0

LIVENESS_CHECK_COUNTER = LIVENESS_CHECK_INTERVAL / SPOTIFY_CHECK_INTERVAL

stdout_bck = None
csvfieldnames = ['Date', 'Artist', 'Track', 'Playlist', 'Album', 'Last activity']

CLI_CONFIG_PATH = None

# to solve the issue: 'SyntaxError: f-string expression part cannot include a backslash'
nl_ch = "\n"


import sys

if sys.version_info < (3, 6):
    print("* Error: Python version 3.6 or higher required !")
    sys.exit(1)

import time
from time import time_ns
import string
import json
import os
from datetime import datetime
from dateutil import relativedelta
import calendar
import requests as req
import signal
import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import csv
from urllib.parse import quote_plus, quote, urlparse
import subprocess
import platform
import re
import ipaddress
from html import escape
import base64
import random
import shutil
from pathlib import Path
import secrets
from typing import Optional
from email.utils import parsedate_to_datetime
import uuid #jmk ntfy album/song images
from jmktools.ntfy import send_ntfy as jmk_send_ntfy, NTFY_STATUS_HIDE, NTFY_STATUS, NTFY_ALERTS, NTFY_STATUS_HIDE, NTFY_STATUS, NTFY_ALERTS #jmk ntfy
import sheets_helper

import urllib3
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SESSION = req.Session()

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup #jmk playlist images

# Cap server-provided Retry-After to avoid long blocking sleeps on 429 responses
MAX_RETRY_AFTER_SECONDS = 60


class CappedRetry(Retry):
    def get_retry_after(self, response):
        retry_after = super().get_retry_after(response)
        if retry_after is None:
            return None
        return min(retry_after, MAX_RETRY_AFTER_SECONDS)


retry = CappedRetry(
    total=5,
    connect=3,
    read=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "HEAD", "OPTIONS"],
    raise_on_status=False,
    respect_retry_after_header=True
)

adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
SESSION.mount("https://", adapter)
SESSION.mount("http://", adapter)


def build_dz_string(playlist_data):
    name = playlist_data['name']
    count_start = playlist_data['count_start']
    count_shuffle = playlist_data['count_shuffle']
    shuffle_details = f"({count_shuffle} via smart shuffle)" if count_shuffle > 0 else ""
    print_debug(f"BUILDING DZ -> name: {name}, count_start: {count_start}, count_shuffle: {count_shuffle}")
    print_debug(f"BUILDING DZ -> shuffle_details: {shuffle_details}")
    print_debug(f"BUILDING DZ -> override: {count_overridden}")
    if count_start < playlist_data['qty_start']:
        print_debug(f"CLEARING DZ DUE TO START_CNT < QTY_CNT -> name: {name}, count_start: {count_start}, count_end: {playlist_data['qty_start']}")
        return ""
    if count_overridden:
        count_start -= (playlist_data['qty_start'] - 1)
    return f"Playlist '{name}' Count: {count_start} {shuffle_details}"


# Truncates each line of a string to a specified number of characters including tab expansion and multi-line support
def truncate_string_per_line(message, truncate_width, tabsize=8):
    try:
        from wcwidth import wcwidth
    except ImportError:
        return message

    lines = message.split('\n')
    truncated_lines = []

    for line in lines:
        expanded_line = line.expandtabs(tabsize)
        current_width = 0
        truncated = ''

        for char in expanded_line:
            char_width = wcwidth(char)
            if char_width < 0:
                char_width = 0  # Non-printable or unknown width
            if current_width + char_width > truncate_width:
                break
            truncated += char
            current_width += char_width

        truncated_lines.append(truncated)

    return '\n'.join(truncated_lines)


# Logger class to output messages to stdout and log file
class Logger(object):
    def __init__(self, filename, mode="both"):
        self.terminal = sys.stdout
        if not DISABLE_LOGGING:
            self.logfile = open(filename, "a", buffering=1, encoding="utf-8")
        self.mode = mode  # Controls where to print

    def write(self, message):
        """Write message based on the selected mode."""
        if not DISABLE_LOGGING:
            if self.mode in ["both", "log"]:
                self.logfile.write(message.expandtabs(8))
                self.logfile.flush()
        if self.mode in ["both", "screen"]:
            if (TRUNCATE_CHARS):
                message = truncate_string_per_line(message, TRUNCATE_CHARS)
            self.terminal.write(message.expandtabs(8))
            self.terminal.flush()

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

# Helper functions using persistent loggers
def print_to_log(message):
    """Prints only to the log file."""
##jmkfix
    if not ALT_VIEW:
        sys.__stdout__.write(str(message).expandtabs(8) + "\n")  # Force writing to actual console
        sys.__stdout__.flush()
    else:
        if not DISABLE_LOGGING:
            log_logger.write(str(message).expandtabs(8) + "\n")

def print_to_both(message):
    """Prints to both the log file and screen, bypassing sys.stdout redirection."""
    if not DISABLE_LOGGING:
        log_logger.write(str(message).expandtabs(8) + "\n")
    if (TRUNCATE_CHARS):
        message = truncate_string_per_line(message.expandtabs(8), TRUNCATE_CHARS)
    sys.__stdout__.write(str(message) + "\n")  # Force writing to actual console
    sys.__stdout__.flush()

# DEBUG_JMK: 0 = disabled, 1 = log only, 2 = screen & log, 3 = screen only
def print_to_screen(message):
    """Prints only to the screen, bypassing sys.stdout redirection, unless debugging."""
    if DEBUG_JMK in (1, 2):
        if log_logger:
            log_logger.write(str(message).expandtabs(8) + "\n")
    if (TRUNCATE_CHARS):
        message = truncate_string_per_line(message.expandtabs(8), TRUNCATE_CHARS)
    sys.__stdout__.write(str(message) + "\n")  # Force writing to actual console
    sys.__stdout__.flush()

# DEBUG_JMK: 0 = disabled, 1 = log only, 2 = screen & log, 3 = screen only
def print_debug(message):
    """Prints to the log file and/or screen, depending on configuration."""
    if DEBUG_JMK:
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[DEBUG {timestamp}] {message}"
        if not DISABLE_LOGGING:
            if DEBUG_JMK in (1, 2):
                log_logger.write(str(message).expandtabs(8) + "\n")
        if DEBUG_JMK in (2, 3):
            if (TRUNCATE_CHARS):
                message = truncate_string_per_line(message.expandtabs(8), TRUNCATE_CHARS)
            sys.__stdout__.write(str(message) + "\n")  # Force writing to actual console
            sys.__stdout__.flush()

def timestring():
    now = datetime.now()
    return now.strftime("%m/%d, %H:%M:%S")

def send_ntfy(message, image_url, track, artist, album, playlist, timediffstr, count):
# KEL, 08/11, 20:25:28: START: September - Earth, Wind & Fire (The Best Of Earth, Wind & Fire Vol. 1) [YACHT ROCK | TOP 100 SONGS]
# END: [00]: Nobody But You (Duet with Gwen Stefani) - Blake Shelton (Fully Loaded: God's Country) [Discovery zone], Song Count: 1
# f"{sp_track.strip()} - {sp_artist.strip()} ({sp_album.strip()}) [{sp_playlist.strip()}]{iconstring()}"
# send_notification(f"END: [{time_diff_str()}]: {songstring()}, Song Count: {listened_songs}", sp_album_image_url)
# send_notification(dz_message, "", track, artist, album, playlist, "", notify_playlist['count_start'])
    # icon = ""

    priority_kel      = 1
    priority_kel_lo   = 1
    priority_kel_hi   = 4
    priority_kel_dz   = 5

    priority_jmk      = 1
    priority_jmk_lo   = 1
    priority_jmk_hi   = 1
    priority_jmk_dz   = 1

    emoji = ""
    
    if ERR_CODE == "KEL":
        topic = NTFY_TOPIC_KEL
        priority        = priority_kel
        priority_start  = priority_kel_hi
        priority_stop   = priority_kel_lo
        priority_dz     = priority_kel_dz
        priority_dz_off = priority_kel_lo
        priority_liked  = priority_kel_lo
    elif ERR_CODE == "JMK":
        topic = NTFY_TOPIC_JMK
        priority        = priority_jmk
        priority_start  = priority_jmk_hi
        priority_stop   = priority_jmk_lo
        priority_dz     = priority_jmk_dz
        priority_dz_off = priority_jmk_lo
        priority_liked  = priority_jmk_lo
    else:
        priority        = 1 # shouldn't happen, but just in case
        priority_start  = 1 # shouldn't happen, but just in case
        priority_stop   = 1 # shouldn't happen, but just in case
        priority_dz     = 1 # shouldn't happen, but just in case
        priority_dz_off = 1 # shouldn't happen, but just in case
        priority_liked  = 1 # shouldn't happen, but just in case
    
    icon      = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/250px-Spotify_icon.svg.png"
    ICON_DZ   = "https://em-content.zobj.net/source/facebook/65/heavy-black-heart_2764.png"
    URL_DZ    = "https://mosaic.scdn.co/300/ab67616d00001e02176e29e598499208ff338ae1ab67616d00001e021daec881d1e9fd2fa7c2d009ab67616d00001e022519d01c0cca06f134eeadd8ab67616d00001e028cae5034066af45cdfbc4266"
    URL_LIKED = "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000da8470d229cb865e8d81cdce0889"

    if not playlist:
        playlist = "unknown playlist"
    print_debug(f"send_ntfy_msg -> {message}")
    print_debug(f"send_ntfy_url -> {image_url}")
    if (message[0:3] == "***") and ("Discovery Zone" in message):
        if "' Detected" in message:
            title = f"Playlist '{playlist}' Detected"
            body = f"{track}\n{artist}\n{album}\n[{playlist}]"
            image_url = URL_DZ
            icon = ICON_DZ
            emoji = "heart"       
            priority = priority_dz # change priority from default
        elif "' Cleared" in message:
            title = f"Playlist '{playlist}' Cleared"
            body = f"{track}\n{artist}\n{album}"
            image_url = URL_DZ
            icon = ICON_DZ
            emoji = "heart"       
            #priority = priority_dz_off # change priority from default
        print_debug(f"send_ntfy_url -> {image_url}")

    elif (message[0:3] == "***") and ("Liked Songs" in message):
        if "' Detected" in message:
            title = f"Playlist '{playlist}' Detected"
            body = f"{track}\n{artist}\n{album}\n[{playlist}]"
            image_url = URL_LIKED
            emoji = "blue_heart"       
            #priority = priority_liked # change priority from default
        elif "' Cleared" in message:
            title = f"Playlist '{playlist}' Cleared"
            body = f"{track}\n{artist}\n{album}"
            image_url = URL_LIKED
            emoji = "blue_heart"       
            #priority = priority_liked # change priority from default

    elif (message[0:5] == "START"):
        title = f'{ERR_CODE} started streaming'
        if playlist == "unknown playlist":
            body = f"{track}\n{artist}\n{album}"
        else:
            body = f"{track}\n{artist}\n{album}\n[{playlist}]"
        emoji = "green_circle"
        priority = priority_start # change priority from default

    elif (message[0:3] == "END"):
        title = f'{ERR_CODE} stopped @ {timediffstr} mins & {count} songs'
        if playlist == "unknown playlist":
            body = f"{track}\n{artist}\n{album}"
        else:
            body = f"{track}\n{artist}\n{album}\n[{playlist}]"
        emoji = "stop_sign"
        priority = priority_stop # change priority from default

    else:
        body = ""
        title = f'{ERR_CODE} @ {timediffstr} mins & {count} songs'
        if playlist == "unknown playlist":
            body = f"{track}\n{artist}\n{album}"
        else:
            body = f"{track}\n{artist}\n{album}\n[{playlist}]"

    """
    Resizes an image, saves it to a unique file, and sends a multi-line
    notification with the image attached via a public URL.
    """
    # Define your local and public paths
    local_directory = r"C:\inetpub\wwwroot\krontz.com\spotify"
    public_base_url = "https://krontz.nakattack.com/spotify/"
    
    # Ensure the local directory exists
    if not os.path.exists(local_directory):
        print(f"Error: The directory {local_directory} does not exist. Please create it.")
        return

    if NTFY_IMAGES and image_url: # don't do this if ""
        try:
            # Step 1: Download and process the image
            print_debug(f"NTFY Downloading image... {image_url}")
            response = req.get(image_url)
            response.raise_for_status()
            
            content_fit = (160, 160)
            original_img = Image.open(BytesIO(response.content))
            print_debug(f"NTFY Original image dimensions: {original_img.size}")
            resized_img = original_img.copy()
            resized_img.thumbnail(content_fit, Image.LANCZOS)
            print_debug(f"NTFY Resized image dimensions: {resized_img.size}")
            
            target_size=(400, 160)
            # background_color="black"
            background_color=(27, 32, 35)
            canvas = Image.new("RGB", target_size, background_color)
            
            paste_x = (target_size[0] - resized_img.size[0]) // 2
            paste_y = (target_size[1] - resized_img.size[1]) // 2
            
            canvas.paste(resized_img, (paste_x, paste_y))

            # Step 2: Save the image with a unique filename
            unique_filename = f"{uuid.uuid4().hex}.jpeg"
            full_local_path = os.path.join(local_directory, unique_filename)
            
            print_debug(f"NTFY Saving resized image to: {full_local_path}")
            canvas.save(full_local_path, format='JPEG')
            
            # Step 3: Construct the public URL for the 'Attach' header
            attach_url = f"{public_base_url}{unique_filename}"
            
            # print_debug("NTFY Notification sent successfully! ✅")

        except req.exceptions.RequestException as e:
            print_debug(f"NTFY: Image generation error: {e}")
        except Exception as e:
            print_debug(f"NTFY: Image generation error: {e}")
    else:
        attach_url = ""

    try:
        # Prepare the ntfy request
        # Step 4: Send the ntfy request with the multi-line message in the body
        print_debug(f"Sending notification, NTFY Body: {body}")

        if jmk_send_ntfy(title, body, topic=topic, priority=priority, tags=emoji, attach=attach_url, verbose=0, verify_verbose=0):
            print_debug(f"NTFY Notification sent successfully! ✅: {body}")
 
    except Exception as e:
        debug_print(f"NTFY: An unexpected error occurred: {e}")
        img_error = True
    

def send_notification(message, image_url="", track="", artist="", album="", playlist="", timediffstr="", count=0):
    send_ntfy(message, image_url, track.strip(), artist.strip(), album.strip(), playlist.strip(), timediffstr.strip(), count)
    

def spotify_get_playlist_items(access_token, playlist_uri, fields, limit, offset, oauth_app=False):
    print_debug(f"spotify_get_playlist_items")
    print_debug(f"access_token: {access_token}")
    # print_debug(f"oauth_app: {oauth_app}")
    playlist_id = playlist_uri.split(':', 2)[2]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields={fields}&limit={limit}&offset={offset}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie" and not oauth_app:
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })

    # add si parameter so link opens in native Spotify app after clicking
    si = "?si=1"

    try:
        response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        print_debug(f"spotify_get_playlist_items")
        print_debug(f"{response}")
        print_debug(f"{response.json()}")
        response.raise_for_status()
        return response.json()
    except Exception:
        raise


def search_playlist(access_token, search_playlist_name, search_playlist_uri, search_song_id, search_track_name, search_artist_name, show_size):
    playlist_size = 9999
    playlist_offset = 0
    playlist_limit = 100
    found_track = False

    try:
#        if search_playlist_name.upper() in {LIKED_PLAYLIST_NAME.upper(), DZ_PLAYLIST_NAME.upper()}:
        if search_playlist_name.upper() in {LIKED_PLAYLIST_NAME.upper()}:
            return True
        
        print_debug(f"SEARCHING PLAYLIST -> search_playlist_name: {search_playlist_name}, search_track_name: {search_track_name}, search_artist_name: {search_artist_name}")
        print_debug(f"SEARCHING PLAYLIST -> search_playlist_uri: {search_playlist_uri}, search_song_id: {search_song_id}")
        print_debug(f"-- playlist_offset: {playlist_offset}, playlist_size: {playlist_size}")

        while playlist_offset < playlist_size and not found_track:
            context_json = spotify_get_playlist_items(access_token, search_playlist_uri, "total,items(track(id,name,artists))", playlist_limit, playlist_offset, oauth_app=True)
            playlist_size = context_json.get("total", playlist_size)

            # print_debug(f"-- context_json: {context_json}")
            # print_debug(f"-- playlist_offset: {playlist_offset}, playlist_size: {playlist_size}")

            if not context_json or 'items' not in context_json:
                debug_print("searchPlaylist error: No items in playlist response")
                break

            if show_size and playlist_offset == 0:
                debug_print(f"playlist size: {playlist_size}")

            # Updated search logic per 3/28/2025 ChatGPT change to check all artists not just [0]
            found_track = any(
                item["track"]["id"] == search_song_id or 
                (item["track"]["name"] == search_track_name and any(artist["name"] == search_artist_name for artist in item["track"]["artists"]))
                for item in context_json["items"]
            )

            print_debug(f"-- found_track: {found_track}")

            playlist_offset += playlist_limit

    except Exception as err:
        debug_print(f"searchPlaylist error: {err}")

    return found_track

    
def find_song_in_playlists(song_name: str, current_playlist, playlist_name):
    global count_overridden
    song_name_upper = song_name.upper() # Convert to uppercase for case-insensitive comparison

    # Prioritize playlist name match, then existing playlist, then new playlist
    # 1. Playlist Name Match
    print_debug(f"FIND_SONG_IN_PLAYLIST - NAME MATCH (A) -> {playlist_name}, {song_name}")
    for playlist_data in monitored_playlists_data.values():
        # Detect if playlist name is a match
        if playlist_name and (playlist_name.upper() == playlist_data.get('name', "B").upper()):
            print_debug(f"*** ACTUAL PLAYLIST NAME MATCH!!! (A) *** : {playlist_name} = {playlist_data.get('name', 'MissingB')}, {playlist_data['count_start']}, {playlist_data['qty_start']}")
            if playlist_data['count_start'] < (playlist_data['qty_start'] - 1):
                print_debug(f"*** OVERRIDE COUNT - START NEW PL (A1): from {playlist_data['count_start']} to {playlist_data['qty_start'] - 1}")
                if current_playlist:
                    print_debug(f"*** OVERRIDE COUNT - END LAST PL  (A2): from {current_playlist['count_end']} to {current_playlist['qty_end']}")
                else:
                    print_debug(f"*** OVERRIDE COUNT END SKIPPED - CURRENT PLAYLIST IS FALSE - (A3): {current_playlist}")
                playlist_data['count_start'] = playlist_data['qty_start'] - 1 # gets incremented after return
                count_overridden = True
                if current_playlist:
                    current_playlist['count_end'] = current_playlist['qty_end']
            return playlist_data

    # 2. Check existing playlist for continuity in case track is in multiple monitored playlists
    if current_playlist:
        print_debug(f"FIND_SONG_IN_PLAYLIST - EXISTING PLAYLIST (B) -> {playlist_name}, {song_name}")
        tracks_set = current_playlist.get('tracks_set', False)
        if tracks_set and isinstance(tracks_set, set):
            if song_name_upper in tracks_set:
                print_debug(f"EXISTING PLAYLIST PRIORITY MATCHED!!! (B) : {current_playlist.get('name', 'Missing')}, {song_name}")
                return current_playlist

    # 3. Search for new playlist match 
    print_debug(f"FIND_SONG_IN_PLAYLIST - NEW PLAYLIST (C) -> {playlist_name}, {song_name}")
    for playlist_data in monitored_playlists_data.values():
        tracks_set = playlist_data.get('tracks_set', False)
        if tracks_set and isinstance(tracks_set, set):
            if song_name_upper in tracks_set:
                print_debug(f"FOUND SONG IN MONITORED PLAYLIST -> {playlist_name}, {song_name}")
                return playlist_data 
    
    return False # Song not found in any playlist


def periodic_load_tracks_flexible(playlist_info):
    playlist_name = playlist_info['name']
    filename = playlist_info['filename']
    # Use the 'refresh' key from playlist_info, or fall back to a default
    reload_frequency = playlist_info.get('refresh', LOAD_TRACKS_FREQUENCY)

    def task():
        # Use .get() with a default empty set to handle initial state safely
        old_tracks_set = monitored_playlists_data.get(playlist_name, {}).get('tracks_set', set())
        old_len = len(old_tracks_set)
        
        # Ensure the playlist entry exists in the global dictionary and has a 'tracks_set' key
        if playlist_name not in monitored_playlists_data:
            print_debug(f"FOUND NEW PERIODIC PLAYLIST: {playlist_name}")
            monitored_playlists_data[playlist_name] = playlist_info.copy() # Copy original info
            monitored_playlists_data[playlist_name]['tracks_set'] = set() # Initialize empty set for tracks
            # Initialize new count variables here
            monitored_playlists_data[playlist_name]['count_start'] = 0
            monitored_playlists_data[playlist_name]['count_end'] = 0
            monitored_playlists_data[playlist_name]['count_shuffle'] = 0
        else:
            # print_debug(f"RESCANNING PERIODIC PLAYLIST FOR CHANGES: {playlist_name}")
            pass
        raw_tracks_list = load_spotify_tracks_from_file(filename)
        unique_tracks_set = set()
        duplicates_removed = 0

        for track in raw_tracks_list:
            if track in unique_tracks_set:
                duplicates_removed += 1
            else:
                unique_tracks_set.add(track)

        new_tracks_set = unique_tracks_set
        new_len = len(new_tracks_set)

        # this will be printed only if checked at designated interval and there is a change in the playlist
        if new_tracks_set != old_tracks_set:
            print_debug(f"PERIODIC PLAYLIST CHANGE FOUND - {playlist_info.get('name', 'Missing')}")
            if (abs(new_len-old_len) > MAX_PLAYLIST_DIFFERENTIAL) and not INITIAL_STARTUP:
                msg = f"*** Loading Monitored Tracks ({playlist_name}) Aborted! {get_cur_ts()} -> Playlist changed by {abs(new_len-old_len)} (limit: {MAX_PLAYLIST_DIFFERENTIAL})"
            else:
                monitored_playlists_data[playlist_name]['tracks_set'] = new_tracks_set
                len_str = f" [was: {old_len}] " if old_len else " "
                longest_name_length = max(len(playlist['name']) for playlist in ADD_PLAYLISTS_TO_MONITOR)
                msg_name = f"{playlist_name})" # note extra parenthesis after name
                formatted_msg_name = f"{msg_name:<{longest_name_length + 1}}"
                msg = f"*** Loaded Monitored Tracks ({formatted_msg_name}: {get_cur_ts()} -> {new_len} songs{len_str}[{duplicates_removed} duplicates removed]"

            if INITIAL_STARTUP:
                print_to_both(msg)
            else:
                print_to_log(msg)
        else:
            pass
            # print_debug(f"PERIODIC CHECK - NO PLAYLIST CHANGE DETECTED - {playlist_info.get('name', 'Missing')}")
                
        # Schedule the next run with the specific refresh frequency for this playlist
        if reload_frequency > 0:
            # print_debug(f"SCHEDULING RELOAD @ {reload_frequency} seconds")
            timer = threading.Timer(reload_frequency, task)
            timer.daemon = True
            timer.start()
        else:
            print_debug(f"NOT RELOADING AS FREQ = {reload_frequency}")
        
    task() # Initial call to start the loading process
    

def load_spotify_tracks_from_file(filename):
    tracks = []
    try:
        try:
            with open(filename, encoding="utf-8") as file:
                lines = file.read().splitlines()
        except UnicodeDecodeError:
            with open(filename, encoding="cp1252") as file:
                lines = file.read().splitlines()

        tracks = [
            line.strip().upper()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]
    except Exception as e:
        print(f"* Error: file with Spotify tracks cannot be opened - {e}")
        sys.exit(1)
    return tracks


    def flush(self):
        pass


def flag_file_create():
    try:
        with open(FLAG_FILE, "w") as f:
            f.write("This indicates active streaming by monitored user")
    except Exception:
        pass


def flag_file_delete():
    try:
        if os.path.exists(FLAG_FILE):
            os.remove(FLAG_FILE)
    except Exception:
        pass


# Class used to generate timeout exceptions
class TimeoutException(Exception):
    pass


# Class used when TOTP secrets are unavailable or unusable for token generation
class SecretsUnavailableError(Exception):
    pass


# Signal handler for SIGALRM when the operation times out
def timeout_handler(sig, frame):
    raise TimeoutException


# Signal handler when user presses Ctrl+C
def signal_handler(sig, frame):
    sys.stdout = stdout_bck
    print('\n* You pressed Ctrl+C, tool is terminated.')
    if FLAG_FILE:
        flag_file_delete()
    sys.exit(0)


# Checks internet connectivity
def check_internet(url=CHECK_INTERNET_URL, timeout=CHECK_INTERNET_TIMEOUT, verify=VERIFY_SSL):
    try:
        debug_print(f"HTTP GET {url} [connectivity check], timeout={timeout}, verify_ssl={verify}")
        _ = req.get(url, headers={'User-Agent': USER_AGENT}, timeout=timeout, verify=verify)
        debug_print(f"HTTP GET {url} -> OK")
        return True
    except req.RequestException as e:
        debug_print(f"HTTP GET {url} -> failed: {e}")
        print(f"* No connectivity, please check your network:\n\n{e}")
        return False


# Clears the terminal screen
def clear_screen(enabled=True):
    if not enabled:
        return
    try:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    except Exception:
        print("* Cannot clear the screen contents")


# Debug print helper - only prints when DEBUG_MODE is enabled
def debug_print(message):
    if DEBUG_MODE:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[DEBUG {timestamp}] {message}")


def mask_secret(value, prefix=4, suffix=2):
    if value is None:
        return None
    s = str(value)
    if not s:
        return ""
    if len(s) <= (prefix + suffix):
        return "*" * len(s)
    return f"{s[:prefix]}...{s[-suffix:]}"


def sanitize_debug_params(params):
    if not isinstance(params, dict):
        return params
    redacted_keys = {"totp", "totpServer", "refresh_token", "access_token"}
    out = {}
    for k, v in params.items():
        if k in redacted_keys:
            out[k] = mask_secret(v)
        else:
            out[k] = v
    return out


def sanitize_debug_headers(headers):
    if not isinstance(headers, dict):
        return headers
    sensitive = {"authorization", "cookie", "client-token"}
    out = {}
    for k, v in headers.items():
        if str(k).lower() in sensitive:
            out[k] = mask_secret(v)
        else:
            out[k] = v
    return out


# Converts absolute value of seconds to human readable format
def display_time(seconds, granularity=2):
    intervals = (
        ('years', 31556952),  # approximation
        ('months', 2629746),  # approximation
        ('weeks', 604800),    # 60 * 60 * 24 * 7
        ('days', 86400),      # 60 * 60 * 24
        ('hours', 3600),      # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []

    if seconds > 0:
        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append(f"{value} {name}")
        return ', '.join(result[:granularity])
    else:
        return '0 seconds'


# Calculates time span between two timestamps, accepts timestamp integers, floats and datetime objects
def calculate_timespan(timestamp1, timestamp2, show_weeks=True, show_hours=True, show_minutes=True, show_seconds=True, granularity=3):
    result = []
    intervals = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']
    ts1 = timestamp1
    ts2 = timestamp2

    if type(timestamp1) is int:
        dt1 = datetime.fromtimestamp(int(ts1))
    elif type(timestamp1) is float:
        ts1 = int(round(ts1))
        dt1 = datetime.fromtimestamp(ts1)
    elif type(timestamp1) is datetime:
        dt1 = timestamp1
        ts1 = int(round(dt1.timestamp()))
    else:
        return ""

    if type(timestamp2) is int:
        dt2 = datetime.fromtimestamp(int(ts2))
    elif type(timestamp2) is float:
        ts2 = int(round(ts2))
        dt2 = datetime.fromtimestamp(ts2)
    elif type(timestamp2) is datetime:
        dt2 = timestamp2
        ts2 = int(round(dt2.timestamp()))
    else:
        return ""

    if ts1 >= ts2:
        ts_diff = ts1 - ts2
    else:
        ts_diff = ts2 - ts1
        dt1, dt2 = dt2, dt1

    if ts_diff > 0:
        date_diff = relativedelta.relativedelta(dt1, dt2)
        years = date_diff.years
        months = date_diff.months
        weeks = date_diff.weeks
        if not show_weeks:
            weeks = 0
        days = date_diff.days
        if weeks > 0:
            days = days - (weeks * 7)
        hours = date_diff.hours
        if (not show_hours and ts_diff > 86400):
            hours = 0
        minutes = date_diff.minutes
        if (not show_minutes and ts_diff > 3600):
            minutes = 0
        seconds = date_diff.seconds
        if (not show_seconds and ts_diff > 60):
            seconds = 0
        date_list = [years, months, weeks, days, hours, minutes, seconds]

        for index, interval in enumerate(date_list):
            if interval > 0:
                name = intervals[index]
                if interval == 1:
                    name = name.rstrip('s')
                result.append(f"{interval} {name}")
        return ', '.join(result[:granularity])
    else:
        return '0 seconds'


# Sends email notification
def send_email(subject, body, body_html, use_ssl, smtp_timeout=15):
    fqdn_re = re.compile(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)')
    email_re = re.compile(r'[^@]+@[^@]+\.[^@]+')

    try:
        ipaddress.ip_address(str(SMTP_HOST))
    except ValueError:
        if not fqdn_re.search(str(SMTP_HOST)):
            print("Error sending email - SMTP settings are incorrect (invalid IP address/FQDN in SMTP_HOST)")
            return 1

    try:
        port = int(SMTP_PORT)
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print("Error sending email - SMTP settings are incorrect (invalid port number in SMTP_PORT)")
        return 1

    if not email_re.search(str(SENDER_EMAIL)) or not email_re.search(str(RECEIVER_EMAIL)):
        print("Error sending email - SMTP settings are incorrect (invalid email in SENDER_EMAIL or RECEIVER_EMAIL)")
        return 1

    if not SMTP_USER or not isinstance(SMTP_USER, str) or SMTP_USER == "your_smtp_user" or not SMTP_PASSWORD or not isinstance(SMTP_PASSWORD, str) or SMTP_PASSWORD == "your_smtp_password":
        print("Error sending email - SMTP settings are incorrect (check SMTP_USER & SMTP_PASSWORD configuration options)")
        return 1

    if not subject or not isinstance(subject, str):
        print("Error sending email - SMTP settings are incorrect (subject is not a string or is empty)")
        return 1

    if not body and not body_html:
        print("Error sending email - SMTP settings are incorrect (body and body_html cannot be empty at the same time)")
        return 1

    try:
        if use_ssl:
            ssl_context = ssl.create_default_context()
            smtpObj = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=smtp_timeout)
            smtpObj.starttls(context=ssl_context)
        else:
            smtpObj = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=smtp_timeout)
        smtpObj.login(SMTP_USER, SMTP_PASSWORD)
        email_msg = MIMEMultipart('alternative')
        email_msg["From"] = SENDER_EMAIL
        email_msg["To"] = RECEIVER_EMAIL
        email_msg["Subject"] = str(Header(subject, 'utf-8'))

        if body:
            part1 = MIMEText(body, 'plain')
            part1 = MIMEText(body.encode('utf-8'), 'plain', _charset='utf-8')
            email_msg.attach(part1)

        if body_html:
            part2 = MIMEText(body_html, 'html')
            part2 = MIMEText(body_html.encode('utf-8'), 'html', _charset='utf-8')
            email_msg.attach(part2)

        smtpObj.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_msg.as_string())
        smtpObj.quit()
    except Exception as e:
        print(f"Error sending email: {e}")
        return 1
    return 0


# Text used for the sheet row inserted when a new listening session starts (mirrors the divider
# email sent alongside it); matches the visual divider row previously produced when the Apps
# Script sliced the "SpotifyJ ---------------------------------" subject down to its tail
SPREADSHEET_DIVIDER_TEXT = "-" * 21


# Writes one row to the spreadsheet tab matching the active ERR_CODE (if UPDATE_SPREADSHEET is
# enabled), draining any previously queued rows first. Sends an error email/ntfy alert the moment
# a write failure starts queuing rows, and a recovery email/ntfy alert the moment the queue fully
# drains again - not on every retry in between.
# When want_footer is True, returns the "spreadsheet updated"/"spreadsheet error" text to append
# to a song-change email body (blank strings otherwise, or when UPDATE_SPREADSHEET is disabled).
def update_spreadsheet_row(col_b_text, want_footer):
    if not UPDATE_SPREADSHEET:
        return "", ""

    # Date-only, matching the legacy Apps Script column (which stored msg.getDate() but the sheet
    # displays date-only) - the clock time already lives at the front of col_b_text, so putting a
    # full timestamp here too would be redundant and renders differently (date+time) than the
    # existing rows above it.
    row_ts = datetime.now().strftime("%Y-%m-%d")
    success, entered_error, recovered = sheets_helper.update_spreadsheet(ERR_CODE, SPREADSHEET_ID, ERR_CODE, [row_ts, col_b_text], GOOGLE_OAUTH_CLIENT_FILE, GOOGLE_OAUTH_TOKEN_FILE)

    if entered_error:
        print(f"* Error: failed to update Google Sheet (tab '{ERR_CODE}') - row queued for retry")
        if ERROR_NOTIFICATION:
            err_subject = f"spotify_monitor: failed to update Google Sheet (tab '{ERR_CODE}') - row queued for retry"
            err_body = f"Could not write to the spreadsheet (tab '{ERR_CODE}'). The row has been queued locally and will be retried automatically on the next check.\n\nRow: {row_ts} | {col_b_text}{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
            err_body_html = f"<html><head></head><body>Could not write to the spreadsheet (tab '{escape(ERR_CODE)}'). The row has been queued locally and will be retried automatically on the next check.<br><br>Row: {escape(row_ts)} | {escape(col_b_text)}{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
            send_email(err_subject, err_body, err_body_html, SMTP_SSL)
        if SEND_NOTIFY:
            send_notification(f"spotify_monitor: Google Sheet update failed (tab '{ERR_CODE}') - row queued for retry")
    elif recovered:
        print(f"* Google Sheet (tab '{ERR_CODE}') queue caught up")
        if ERROR_NOTIFICATION:
            rec_subject = f"spotify_monitor: Google Sheet (tab '{ERR_CODE}') caught up"
            rec_body = f"The spreadsheet queue has been fully drained and the sheet (tab '{ERR_CODE}') is now up to date.{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
            rec_body_html = f"<html><head></head><body>The spreadsheet queue has been fully drained and the sheet (tab '{escape(ERR_CODE)}') is now up to date.{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
            send_email(rec_subject, rec_body, rec_body_html, SMTP_SSL)
        if SEND_NOTIFY:
            send_notification(f"spotify_monitor: Google Sheet (tab '{ERR_CODE}') caught up")

    if not want_footer:
        return "", ""
    if success:
        return "\n\nspreadsheet updated", "<br><br>spreadsheet updated"
    return "\n\nspreadsheet error", "<br><br>spreadsheet error"


# Initializes the CSV file
def init_csv_file(csv_file_name):
    try:
        if not os.path.isfile(csv_file_name) or os.path.getsize(csv_file_name) == 0:
            with open(csv_file_name, 'a', newline='', buffering=1, encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=csvfieldnames, quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
    except Exception as e:
        raise RuntimeError(f"Could not initialize CSV file '{csv_file_name}': {e}")


# Writes CSV entry
def write_csv_entry(csv_file_name, timestamp, artist, track, playlist, album, last_activity_ts):
    try:

        with open(csv_file_name, 'a', newline='', buffering=1, encoding="utf-8") as csv_file:
            csvwriter = csv.DictWriter(csv_file, fieldnames=csvfieldnames, quoting=csv.QUOTE_NONNUMERIC)
            csvwriter.writerow({'Date': timestamp, 'Artist': artist, 'Track': track, 'Playlist': playlist, 'Album': album, 'Last activity': last_activity_ts})

    except Exception as e:
        raise RuntimeError(f"Failed to write to CSV file '{csv_file_name}': {e}")


# Returns the current date/time in human readable format; eg. Sun 21 Apr 2024, 15:08:45
def get_cur_ts(ts_str=""):
    return (f'{ts_str}{calendar.day_abbr[(datetime.fromtimestamp(int(time.time()))).weekday()]} {datetime.fromtimestamp(int(time.time())).strftime("%d %b %Y, %H:%M:%S")}')


# Prints the current date/time in human readable format with separator; eg. Sun 21 Apr 2024, 15:08:45
def print_cur_ts(ts_str=""):
    print(get_cur_ts(str(ts_str)))
    print("─" * HORIZONTAL_LINE)


# Returns the timestamp/datetime object in human readable format (long version); eg. Sun 21 Apr 2024, 15:08:45
def get_date_from_ts(ts):
    if type(ts) is datetime:
        ts_new = int(round(ts.timestamp()))
    elif type(ts) is int:
        ts_new = ts
    elif type(ts) is float:
        ts_new = int(round(ts))
    else:
        return ""

    return (f'{calendar.day_abbr[(datetime.fromtimestamp(ts_new)).weekday()]} {datetime.fromtimestamp(ts_new).strftime("%d %b %Y, %H:%M:%S")}')


# Returns the timestamp/datetime object in human readable format (short version); eg.
# Sun 21 Apr 15:08
# Sun 21 Apr 24, 15:08 (if show_year == True and current year is different)
# Sun 21 Apr (if show_hour == False)
def get_short_date_from_ts(ts, show_year=False, show_hour=True):
    if type(ts) is datetime:
        ts_new = int(round(ts.timestamp()))
    elif type(ts) is int:
        ts_new = ts
    elif type(ts) is float:
        ts_new = int(round(ts))
    else:
        return ""

    if show_hour:
        hour_strftime = " %H:%M"
    else:
        hour_strftime = ""

    if show_year and int(datetime.fromtimestamp(ts_new).strftime("%Y")) != int(datetime.now().strftime("%Y")):
        if show_hour:
            hour_prefix = ","
        else:
            hour_prefix = ""
        return (f'{calendar.day_abbr[(datetime.fromtimestamp(ts_new)).weekday()]} {datetime.fromtimestamp(ts_new).strftime(f"%d %b %y{hour_prefix}{hour_strftime}")}')
    else:
        return (f'{calendar.day_abbr[(datetime.fromtimestamp(ts_new)).weekday()]} {datetime.fromtimestamp(ts_new).strftime(f"%d %b{hour_strftime}")}')


# Returns the timestamp/datetime object in human readable format (only hour, minutes and optionally seconds): eg. 15:08:12
def get_hour_min_from_ts(ts, show_seconds=False):
    if type(ts) is datetime:
        ts_new = int(round(ts.timestamp()))
    elif type(ts) is int:
        ts_new = ts
    elif type(ts) is float:
        ts_new = int(round(ts))
    else:
        return ""

    if show_seconds:
        out_strf = "%H:%M:%S"
    else:
        out_strf = "%H:%M"
    return (str(datetime.fromtimestamp(ts_new).strftime(out_strf)))


# Returns the range between two timestamps/datetime objects; eg. Sun 21 Apr 14:09 - 14:15
def get_range_of_dates_from_tss(ts1, ts2, between_sep=" - ", short=False):
    if type(ts1) is datetime:
        ts1_new = int(round(ts1.timestamp()))
    elif type(ts1) is int:
        ts1_new = ts1
    elif type(ts1) is float:
        ts1_new = int(round(ts1))
    else:
        return ""

    if type(ts2) is datetime:
        ts2_new = int(round(ts2.timestamp()))
    elif type(ts2) is int:
        ts2_new = ts2
    elif type(ts2) is float:
        ts2_new = int(round(ts2))
    else:
        return ""

    ts1_strf = datetime.fromtimestamp(ts1_new).strftime("%Y%m%d")
    ts2_strf = datetime.fromtimestamp(ts2_new).strftime("%Y%m%d")

    if ts1_strf == ts2_strf:
        if short:
            out_str = f"{get_short_date_from_ts(ts1_new)}{between_sep}{get_hour_min_from_ts(ts2_new)}"
        else:
            out_str = f"{get_date_from_ts(ts1_new)}{between_sep}{get_hour_min_from_ts(ts2_new, show_seconds=True)}"
    else:
        if short:
            out_str = f"{get_short_date_from_ts(ts1_new)}{between_sep}{get_short_date_from_ts(ts2_new)}"
        else:
            out_str = f"{get_date_from_ts(ts1_new)}{between_sep}{get_date_from_ts(ts2_new)}"
    return (str(out_str))


# Signal handler for SIGUSR1 allowing to switch active/inactive email notifications
def toggle_active_inactive_notifications_signal_handler(sig, frame):
    global ACTIVE_NOTIFICATION
    global INACTIVE_NOTIFICATION
    ACTIVE_NOTIFICATION = not ACTIVE_NOTIFICATION
    INACTIVE_NOTIFICATION = not INACTIVE_NOTIFICATION
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Email notifications: [active = {ACTIVE_NOTIFICATION}] [inactive = {INACTIVE_NOTIFICATION}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGUSR2 allowing to switch every song email notifications
def toggle_song_notifications_signal_handler(sig, frame):
    global SONG_NOTIFICATION
    SONG_NOTIFICATION = not SONG_NOTIFICATION
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Email notifications: [every song = {SONG_NOTIFICATION}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGCONT allowing to switch tracked songs email notifications
def toggle_track_notifications_signal_handler(sig, frame):
    global TRACK_NOTIFICATION
    TRACK_NOTIFICATION = not TRACK_NOTIFICATION
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Email notifications: [tracked = {TRACK_NOTIFICATION}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGPIPE allowing to switch songs on loop email notifications
def toggle_songs_on_loop_notifications_signal_handler(sig, frame):
    global SONG_ON_LOOP_NOTIFICATION
    SONG_ON_LOOP_NOTIFICATION = not SONG_ON_LOOP_NOTIFICATION
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Email notifications: [songs on loop = {SONG_ON_LOOP_NOTIFICATION}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGTRAP allowing to increase inactivity check timer by SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE seconds
def increase_inactivity_check_signal_handler(sig, frame):
    global SPOTIFY_INACTIVITY_CHECK
    SPOTIFY_INACTIVITY_CHECK = SPOTIFY_INACTIVITY_CHECK + SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Spotify timers: [inactivity: {display_time(SPOTIFY_INACTIVITY_CHECK)}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGABRT allowing to decrease inactivity check timer by SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE seconds
def decrease_inactivity_check_signal_handler(sig, frame):
    global SPOTIFY_INACTIVITY_CHECK
    if SPOTIFY_INACTIVITY_CHECK - SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE > 0:
        SPOTIFY_INACTIVITY_CHECK = SPOTIFY_INACTIVITY_CHECK - SPOTIFY_INACTIVITY_CHECK_SIGNAL_VALUE
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")
    print(f"* Spotify timers: [inactivity: {display_time(SPOTIFY_INACTIVITY_CHECK)}]")
    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Signal handler for SIGHUP allowing to reload secrets from dotenv files and token source credentials
# from login & client token requests body files
def reload_secrets_signal_handler(sig, frame):
    global DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN, LOGIN_URL, USER_AGENT, APP_VERSION, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR, CLIENT_MODEL
    
    if isinstance(sig, int):
        sig_name = signal.Signals(sig).name
    else:
        sig_name = sig
    print(f"* Signal {sig_name} received")

    suffix = "\n" if TOKEN_SOURCE == 'client' else ""

    # disable autoscan if DOTENV_FILE set to none
    if DOTENV_FILE and DOTENV_FILE.lower() == 'none':
        env_path = None
    else:
        # reload .env if python-dotenv is installed
        try:
            from dotenv import load_dotenv, find_dotenv
            if DOTENV_FILE:
                env_path = DOTENV_FILE
            else:
                env_path = find_dotenv()
            if env_path:
                load_dotenv(env_path, override=True)
            else:
                print(f"* No .env file found, skipping env-var reload{suffix}")
        except ImportError:
            env_path = None
            print(f"* python-dotenv not installed, skipping env-var reload{suffix}")

    if env_path:
        for secret in SECRET_KEYS:
            old_val = globals().get(secret)
            val = os.getenv(secret)
            if secret == "SP_DC_COOKIE":
                if ALT_COOKIE:
                    val = os.getenv("SP_DC_COOKIE2")
            if secret == "LOGIN_REQUEST_BODY_FILE":
                if ALT_COOKIE:
                    val = os.getenv("LOGIN_REQUEST_BODY_FILE2")
            if val is not None and val != old_val:
                globals()[secret] = val
                print(f"* Reloaded {secret} from {env_path}{suffix}")

    if TOKEN_SOURCE == 'client':

        # Process the login request body file
        if LOGIN_REQUEST_BODY_FILE:
            if os.path.isfile(LOGIN_REQUEST_BODY_FILE):
                try:
                    DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN = parse_login_request_body_file(LOGIN_REQUEST_BODY_FILE)
                except Exception as e:
                    print(f"* Error: Protobuf file ({LOGIN_REQUEST_BODY_FILE}) cannot be processed: {e}")
                else:
                    print(f"* Login data correctly read from Protobuf file ({LOGIN_REQUEST_BODY_FILE}):")
                    print(" - Device ID:\t\t", DEVICE_ID)
                    print(" - System ID:\t\t", SYSTEM_ID)
                    print(" - User URI ID:\t\t", USER_URI_ID)
                    print(" - Refresh Token:\t<<hidden>>\n")
            else:
                print(f"* Error: Protobuf file ({LOGIN_REQUEST_BODY_FILE}) does not exist")

        # Process the client token request body file
        if CLIENTTOKEN_REQUEST_BODY_FILE:
            if os.path.isfile(CLIENTTOKEN_REQUEST_BODY_FILE):
                try:
                    (APP_VERSION, _, _, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR, CLIENT_MODEL) = parse_clienttoken_request_body_file(CLIENTTOKEN_REQUEST_BODY_FILE)
                except Exception as e:
                    print(f"* Error: Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}) cannot be processed: {e}")
                else:
                    print(f"* Client token data correctly read from Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}):")
                    print(" - App version:\t\t", APP_VERSION)
                    print(" - CPU arch:\t\t", CPU_ARCH)
                    print(" - OS build:\t\t", OS_BUILD)
                    print(" - Platform:\t\t", PLATFORM)
                    print(" - OS major:\t\t", OS_MAJOR)
                    print(" - OS minor:\t\t", OS_MINOR)
                    print(" - Client model:\t", CLIENT_MODEL, "\n")
            else:
                print(f"* Error: Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}) does not exist")

    if isinstance(sig, int):
        print_cur_ts("Timestamp:\t\t\t")


# Returns Apple & lyrics search URLs for specified track
def get_apple_genius_search_urls(artist, track):
    spotify_search_string = f"{artist} {track}"
    youtube_music_search_string = quote_plus(spotify_search_string)
    # Clean search string for lyrics services (remove remaster, extended, etc.)
    lyrics_search_string = spotify_search_string
    if re.search(re_search_str, lyrics_search_string, re.IGNORECASE):
        lyrics_search_string = re.sub(re_replace_str, '', lyrics_search_string, flags=re.IGNORECASE)
    apple_search_string = quote(spotify_search_string)
    apple_search_url = f"https://music.apple.com/pl/search?term={apple_search_string}"
    genius_search_url = f"https://genius.com/search?q={quote_plus(lyrics_search_string)}"
    azlyrics_search_url = f"https://www.azlyrics.com/search/?q={quote_plus(lyrics_search_string)}"
    tekstowo_search_url = f"https://www.tekstowo.pl/szukaj,{quote_plus(lyrics_search_string)}.html"
    musixmatch_search_url = f"https://www.musixmatch.com/search?query={quote_plus(lyrics_search_string)}"
    lyrics_com_search_url = f"https://www.lyrics.com/serp.php?st={quote_plus(lyrics_search_string)}&qtype=1"
    youtube_music_search_url = f"https://music.youtube.com/search?q={youtube_music_search_string}"
    amazon_music_search_url = f"https://music.amazon.com/search/{quote_plus(spotify_search_string)}"
    deezer_search_url = f"https://www.deezer.com/search/{quote_plus(spotify_search_string)}"
    tidal_search_url = f"https://tidal.com/search?q={quote_plus(spotify_search_string)}"
    return apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url


# Formats lyrics URLs for console output based on configuration
def format_lyrics_urls_console(genius_url, azlyrics_url, tekstowo_url, musixmatch_url, lyrics_com_url):
    lines = []
    if ENABLE_GENIUS_LYRICS_URL:
        lines.append(f"Genius lyrics URL:\t\t{genius_url}")
    if ENABLE_AZLYRICS_URL:
        lines.append(f"AZLyrics URL:\t\t\t{azlyrics_url}")
    if ENABLE_TEKSTOWO_URL:
        lines.append(f"Tekstowo.pl URL:\t\t{tekstowo_url}")
    if ENABLE_MUSIXMATCH_URL:
        lines.append(f"Musixmatch URL:\t\t\t{musixmatch_url}")
    if ENABLE_LYRICS_COM_URL:
        lines.append(f"Lyrics.com URL:\t\t\t{lyrics_com_url}")
    return "\n".join(lines) if lines else ""


# Formats lyrics URLs for plain text email body based on configuration
def format_lyrics_urls_email_text(genius_url, azlyrics_url, tekstowo_url, musixmatch_url, lyrics_com_url):
    lines = []
    if ENABLE_GENIUS_LYRICS_URL:
        lines.append(f"Genius lyrics URL: {genius_url}")
    if ENABLE_AZLYRICS_URL:
        lines.append(f"AZLyrics URL: {azlyrics_url}")
    if ENABLE_TEKSTOWO_URL:
        lines.append(f"Tekstowo.pl URL: {tekstowo_url}")
    if ENABLE_MUSIXMATCH_URL:
        lines.append(f"Musixmatch URL: {musixmatch_url}")
    if ENABLE_LYRICS_COM_URL:
        lines.append(f"Lyrics.com URL: {lyrics_com_url}")
    return "\n".join(lines) if lines else ""


# Formats lyrics URLs for HTML email body based on configuration
def format_lyrics_urls_email_html(genius_url, azlyrics_url, tekstowo_url, musixmatch_url, lyrics_com_url, artist, track):
    lines = []
    escaped_artist = escape(artist)
    escaped_track = escape(track)
    if ENABLE_GENIUS_LYRICS_URL:
        lines.append(f'Genius lyrics URL: <a href="{genius_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_AZLYRICS_URL:
        lines.append(f'AZLyrics URL: <a href="{azlyrics_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_TEKSTOWO_URL:
        lines.append(f'Tekstowo.pl URL: <a href="{tekstowo_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_MUSIXMATCH_URL:
        lines.append(f'Musixmatch URL: <a href="{musixmatch_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_LYRICS_COM_URL:
        lines.append(f'Lyrics.com URL: <a href="{lyrics_com_url}">{escaped_artist} - {escaped_track}</a>')
    return "<br>".join(lines) if lines else ""


# Formats music service URLs for console output based on configuration
def format_music_urls_console(apple_music_url, youtube_music_url, amazon_music_url, deezer_url, tidal_url):
    lines = []
    if ENABLE_APPLE_MUSIC_URL:
        lines.append(f"Apple Music URL:\t\t{apple_music_url}")
    if ENABLE_YOUTUBE_MUSIC_URL:
        lines.append(f"YouTube Music URL:\t\t{youtube_music_url}")
    if ENABLE_AMAZON_MUSIC_URL:
        lines.append(f"Amazon Music URL:\t\t{amazon_music_url}")
    if ENABLE_DEEZER_URL:
        lines.append(f"Deezer URL:\t\t\t{deezer_url}")
    if ENABLE_TIDAL_URL:
        lines.append(f"Tidal URL:\t\t\t{tidal_url}")
    return "\n".join(lines) if lines else ""


# Formats music service URLs for plain text email body based on configuration
def format_music_urls_email_text(apple_music_url, youtube_music_url, amazon_music_url, deezer_url, tidal_url):
    lines = []
    if ENABLE_APPLE_MUSIC_URL:
        lines.append(f"Apple Music URL: {apple_music_url}")
    if ENABLE_YOUTUBE_MUSIC_URL:
        lines.append(f"YouTube Music URL: {youtube_music_url}")
    if ENABLE_AMAZON_MUSIC_URL:
        lines.append(f"Amazon Music URL: {amazon_music_url}")
    if ENABLE_DEEZER_URL:
        lines.append(f"Deezer URL: {deezer_url}")
    if ENABLE_TIDAL_URL:
        lines.append(f"Tidal URL: {tidal_url}")
    return "\n".join(lines) if lines else ""


# Formats music service URLs for HTML email body based on configuration
def format_music_urls_email_html(apple_music_url, youtube_music_url, amazon_music_url, deezer_url, tidal_url, artist, track):
    lines = []
    escaped_artist = escape(artist)
    escaped_track = escape(track)
    if ENABLE_APPLE_MUSIC_URL:
        lines.append(f'Apple Music URL: <a href="{apple_music_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_YOUTUBE_MUSIC_URL:
        lines.append(f'YouTube Music URL: <a href="{youtube_music_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_AMAZON_MUSIC_URL:
        lines.append(f'Amazon Music URL: <a href="{amazon_music_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_DEEZER_URL:
        lines.append(f'Deezer URL: <a href="{deezer_url}">{escaped_artist} - {escaped_track}</a>')
    if ENABLE_TIDAL_URL:
        lines.append(f'Tidal URL: <a href="{tidal_url}">{escaped_artist} - {escaped_track}</a>')
    return "<br>".join(lines) if lines else ""


# Sends a lightweight request to check Spotify token validity
def check_token_validity(access_token: str, client_id: Optional[str] = None, user_agent: Optional[str] = None, oauth_app: Optional[bool] = False) -> bool:
    url1 = "https://guc-spclient.spotify.com/presence-view/v1/buddylist"
    # Use a known stable track for validation (Bohemian Rhapsody - Queen)
    url2 = "https://api.spotify.com/v1/tracks/7tFiyTwD0nx5a1eklYtX2J"

    url = url2 if oauth_app else url1
    check_mode = "oauth_app" if oauth_app else f"{TOKEN_SOURCE}_token"

    headers = {"Authorization": f"Bearer {access_token}"}

    if user_agent is not None:
        headers.update({
            "User-Agent": user_agent
        })

    if not oauth_app and TOKEN_SOURCE == "cookie" and client_id is not None:
        headers.update({
            "Client-Id": client_id
        })

    if platform.system() != 'Windows':
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(FUNCTION_TIMEOUT + 2)
    try:
        debug_print(
            f"Token validity check mode={check_mode}, url={url}, "
            f"client_id_header={'yes' if 'Client-Id' in headers else 'no'}"
        )
        debug_print(f"HTTP GET {url} [token validity] headers={sanitize_debug_headers(headers)}")
        response = req.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        valid = response.status_code == 200
        debug_print(f"HTTP GET {url} -> {response.status_code} [token validity mode={check_mode}] (valid={valid})")
    except Exception:
        valid = False
        debug_print(f"HTTP GET {url} -> failed during token validity check [mode={check_mode}]")
    finally:
        if platform.system() != 'Windows':
            signal.alarm(0)
    return valid


# -------------------------------------------------------
# Supporting functions when token source is set to cookie
# -------------------------------------------------------

# Returns random user agent string
def get_random_user_agent() -> str:
    browser = random.choice(['chrome', 'firefox', 'edge', 'safari'])

    if browser == 'chrome':
        os_choice = random.choice(['mac', 'windows'])
        if os_choice == 'mac':
            return (
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(4, 9)}) "
                f"AppleWebKit/{random.randrange(530, 537)}.{random.randrange(30, 37)} (KHTML, like Gecko) "
                f"Chrome/{random.randrange(80, 105)}.0.{random.randrange(3000, 4500)}.{random.randrange(60, 125)} "
                f"Safari/{random.randrange(530, 537)}.{random.randrange(30, 36)}"
            )
        else:
            chrome_version = random.randint(80, 105)
            build = random.randint(3000, 4500)
            patch = random.randint(60, 125)
            return (
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_version}.0.{build}.{patch} Safari/537.36"
            )

    elif browser == 'firefox':
        os_choice = random.choice(['windows', 'mac', 'linux'])
        version = random.randint(90, 110)
        if os_choice == 'windows':
            return (
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{version}.0) "
                f"Gecko/20100101 Firefox/{version}.0"
            )
        elif os_choice == 'mac':
            return (
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(0, 10)}; rv:{version}.0) "
                f"Gecko/20100101 Firefox/{version}.0"
            )
        else:
            return (
                f"Mozilla/5.0 (X11; Linux x86_64; rv:{version}.0) "
                f"Gecko/20100101 Firefox/{version}.0"
            )

    elif browser == 'edge':
        os_choice = random.choice(['windows', 'mac'])
        chrome_version = random.randint(80, 105)
        build = random.randint(3000, 4500)
        patch = random.randint(60, 125)
        version_str = f"{chrome_version}.0.{build}.{patch}"
        if os_choice == 'windows':
            return (
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{version_str} Safari/537.36 Edg/{version_str}"
            )
        else:
            return (
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(0, 10)}) "
                f"AppleWebKit/605.1.15 (KHTML, like Gecko) "
                f"Version/{random.randint(13, 16)}.0 Safari/605.1.15 Edg/{version_str}"
            )

    elif browser == 'safari':
        os_choice = 'mac'
        if os_choice == 'mac':
            mac_major = random.randrange(11, 16)
            mac_minor = random.randrange(0, 10)
            webkit_major = random.randint(600, 610)
            webkit_minor = random.randint(1, 20)
            webkit_patch = random.randint(1, 20)
            safari_version = random.randint(13, 16)
            return (
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{mac_major}_{mac_minor}) "
                f"AppleWebKit/{webkit_major}.{webkit_minor}.{webkit_patch} (KHTML, like Gecko) "
                f"Version/{safari_version}.0 Safari/{webkit_major}.{webkit_minor}.{webkit_patch}"
            )
        else:
            return ""
    else:
        return ""


# Returns Spotify edge-server Unix time
def fetch_server_time(session: req.Session, ua: str) -> int:

    headers = {
        "User-Agent": ua,
        "Accept": "*/*",
    }

    try:
        if platform.system() != 'Windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(FUNCTION_TIMEOUT + 2)
        debug_print(f"HTTP HEAD {SERVER_TIME_URL} [server time] timeout={FUNCTION_TIMEOUT}")
        response = session.head(SERVER_TIME_URL, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        response.raise_for_status()
        debug_print(f"HTTP HEAD {SERVER_TIME_URL} -> {response.status_code}")
    except TimeoutException as e:
        raise Exception(f"fetch_server_time() head network request timeout after {display_time(FUNCTION_TIMEOUT + 2)}: {e}")
    except Exception as e:
        raise Exception(f"fetch_server_time() head network request error: {e}")
    finally:
        if platform.system() != 'Windows':
            signal.alarm(0)

    date_hdr = response.headers.get("Date")
    if not date_hdr:
        raise Exception("fetch_server_time() missing 'Date' header")

    return int(parsedate_to_datetime(date_hdr).timestamp())


# Resolves the effective TOTP version, falling back to the highest available when the configured TOTP_VER is missing from SECRET_CIPHER_DICT
def resolve_totp_ver() -> int:
    if not SECRET_CIPHER_DICT:
        raise SecretsUnavailableError("resolve_totp_ver(): SECRET_CIPHER_DICT is empty")
    if TOTP_VER and str(TOTP_VER) in SECRET_CIPHER_DICT:
        return TOTP_VER
    available = sorted(map(int, SECRET_CIPHER_DICT))
    fallback = available[-1]
    if TOTP_VER:
        print(f"Warning: configured TOTP_VER ({TOTP_VER}) is missing from SECRET_CIPHER_DICT (available: {available}); falling back to auto-selected version {fallback}")
    return fallback


# Creates a TOTP object using a secret derived from transformed cipher bytes
def generate_totp():
    import pyotp

    ver = resolve_totp_ver()

    secret_cipher_bytes = SECRET_CIPHER_DICT[str(ver)]

    transformed = [e ^ ((t % 33) + 9) for t, e in enumerate(secret_cipher_bytes)]
    joined = "".join(str(num) for num in transformed)
    hex_str = joined.encode().hex()
    secret = base64.b32encode(bytes.fromhex(hex_str)).decode().rstrip("=")

    return pyotp.TOTP(secret, digits=6, interval=30)


def fetch_and_update_secrets():
    global SECRET_CIPHER_DICT

    if not SECRET_CIPHER_DICT_URL:
        return False

    try:
        if SECRET_CIPHER_DICT_URL.startswith("file:"):
            import os
            from urllib.parse import urlparse, unquote

            parsed = urlparse(SECRET_CIPHER_DICT_URL)

            if parsed.netloc:
                raw_path = f"/{parsed.netloc}{parsed.path or ''}"
            else:
                if SECRET_CIPHER_DICT_URL.startswith("file://"):
                    raw_path = parsed.path or SECRET_CIPHER_DICT_URL[len("file://"):]
                else:
                    raw_path = parsed.path or SECRET_CIPHER_DICT_URL[len("file:"):]

            raw_path = unquote(raw_path)

            if raw_path.startswith("/~"):
                raw_path = raw_path[1:]

            if not raw_path.startswith("/") and not raw_path.startswith("~"):
                raw_path = "/" + raw_path

            path = os.path.expanduser(os.path.expandvars(raw_path))

            print(f"Loading Spotify web-player TOTP secrets from file: {path}")
            if os.path.getsize(path) == 0:
                raise ValueError(f"Secret file is empty: {path}")
            with open(path, "r", encoding="utf-8") as f:
                secrets = json.load(f)
            print("─" * HORIZONTAL_LINE)
        else:
            print(f"Fetching Spotify web-player TOTP secrets from URL: {SECRET_CIPHER_DICT_URL}")
            debug_print(f"HTTP GET {SECRET_CIPHER_DICT_URL} [secrets update]")
            response = req.get(SECRET_CIPHER_DICT_URL, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
            response.raise_for_status()
            debug_print(f"HTTP GET {SECRET_CIPHER_DICT_URL} -> {response.status_code}")
            if not response.text.strip():
                raise ValueError("Fetched payload is empty")
            secrets = response.json()
            print("─" * HORIZONTAL_LINE)

        if not isinstance(secrets, dict) or not secrets:
            raise ValueError("Fetched payload not a non-empty dict")

        for key, value in secrets.items():
            if not isinstance(key, str) or not key.isdigit():
                raise ValueError(f"Invalid key format: {key}")
            if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
                raise ValueError(f"Invalid value format for key {key}")

        SECRET_CIPHER_DICT = secrets
        return True

    except json.JSONDecodeError as e:
        print(f"fetch_and_update_secrets(): Failed to parse secrets (invalid JSON format): {e}")
        return False
    except Exception as e:
        print(f"fetch_and_update_secrets(): Failed to get new secrets: {e}")
        return False


# Refreshes the Spotify access token using the sp_dc cookie, tries first with mode "transport" and if needed with "init"
def refresh_access_token_from_sp_dc(sp_dc: str) -> dict:
    transport = True
    init = True
    session = req.Session()
    data: dict = {}
    token = ""

    server_time = fetch_server_time(session, USER_AGENT)
    totp_obj = generate_totp()
    client_time = int(time_ns() / 1000 / 1000)
    otp_value = totp_obj.at(server_time)

    totp_ver = resolve_totp_ver()

    params = {
        "reason": "transport",
        "productType": "web-player",
        "totp": otp_value,
        "totpServer": otp_value,
        "totpVer": totp_ver,
    }

    if totp_ver < 10:
        params.update({
            "sTime": server_time,
            "cTime": client_time,
            "buildDate": time.strftime("%Y-%m-%d", time.gmtime(server_time)),
            "buildVer": f"web-player_{time.strftime('%Y-%m-%d', time.gmtime(server_time))}_{server_time * 1000}_{secrets.token_hex(4)}",
        })

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Referer": "https://open.spotify.com/",
        "App-Platform": "WebPlayer",
        "Cookie": f"sp_dc={sp_dc}",
    }

    last_err = ""

    try:
        if platform.system() != "Windows":
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(FUNCTION_TIMEOUT + 2)

        debug_print(f"HTTP GET {TOKEN_URL} [sp_dc transport] params={sanitize_debug_params(params)} headers={sanitize_debug_headers(headers)}")
        response = session.get(TOKEN_URL, params=params, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        response.raise_for_status()
        data = response.json()
        token = data.get("accessToken", "")
        debug_print(f"HTTP GET {TOKEN_URL} [sp_dc transport] -> {response.status_code}, token_len={len(token)}")

    except (req.RequestException, TimeoutException, req.HTTPError, ValueError) as e:
        transport = False
        last_err = str(e)
        debug_print(f"HTTP GET {TOKEN_URL} [sp_dc transport] failed: {e}")
    finally:
        if platform.system() != "Windows":
            signal.alarm(0)

    if not transport or (transport and not check_token_validity(token, data.get("clientId", ""), USER_AGENT)):
        params["reason"] = "init"

        try:
            if platform.system() != "Windows":
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(FUNCTION_TIMEOUT + 2)

            debug_print(f"HTTP GET {TOKEN_URL} [sp_dc init] params={sanitize_debug_params(params)} headers={sanitize_debug_headers(headers)}")
            response = session.get(TOKEN_URL, params=params, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
            response.raise_for_status()
            data = response.json()
            token = data.get("accessToken", "")
            debug_print(f"HTTP GET {TOKEN_URL} [sp_dc init] -> {response.status_code}, token_len={len(token)}")

        except (req.RequestException, TimeoutException, req.HTTPError, ValueError) as e:
            init = False
            last_err = str(e)
            debug_print(f"HTTP GET {TOKEN_URL} [sp_dc init] failed: {e}")
        finally:
            if platform.system() != "Windows":
                signal.alarm(0)

    if not init or not data or "accessToken" not in data:
        raise Exception(f"refresh_access_token_from_sp_dc(): Unsuccessful token request{': ' + last_err if last_err else ''}")

    return {
        "access_token": token,
        "expires_at": data["accessTokenExpirationTimestampMs"] // 1000,
        "client_id": data.get("clientId", ""),
        "length": len(token)
    }


# Fetches Spotify access token based on provided SP_DC value
def spotify_get_access_token_from_sp_dc(sp_dc: str):
    global SP_CACHED_ACCESS_TOKEN, SP_ACCESS_TOKEN_EXPIRES_AT, SP_CACHED_CLIENT_ID

    now = time.time()

    if SP_CACHED_ACCESS_TOKEN and now < SP_ACCESS_TOKEN_EXPIRES_AT and check_token_validity(SP_CACHED_ACCESS_TOKEN, SP_CACHED_CLIENT_ID, USER_AGENT):
        debug_print("Using cached Spotify access token (sp_dc source)")
        return SP_CACHED_ACCESS_TOKEN

    if not SECRET_CIPHER_DICT:
        debug_print("SECRET_CIPHER_DICT is empty, fetching secrets before token refresh")
        if not fetch_and_update_secrets():
            raise RuntimeError("Failed to obtain TOTP secrets: SECRET_CIPHER_DICT is empty and secrets update failed")

    max_retries = TOKEN_MAX_RETRIES
    retry = 0

    last_error = ""

    while retry < max_retries:
        try:
            debug_print(f"Refreshing Spotify access token via sp_dc (attempt {retry + 1}/{max_retries})")
            token_data = refresh_access_token_from_sp_dc(sp_dc)
            token = token_data["access_token"]
            client_id = token_data.get("client_id", "")
            length = token_data["length"]

            SP_CACHED_ACCESS_TOKEN = token
            SP_ACCESS_TOKEN_EXPIRES_AT = token_data["expires_at"]
            SP_CACHED_CLIENT_ID = client_id

            if SP_CACHED_ACCESS_TOKEN is None or not check_token_validity(SP_CACHED_ACCESS_TOKEN, SP_CACHED_CLIENT_ID, USER_AGENT):
                debug_print("Received token is invalid, retrying")
                retry += 1
                time.sleep(TOKEN_RETRY_TIMEOUT)
            else:
                debug_print(f"Spotify access token obtained successfully, length={length}")
                break
        except SecretsUnavailableError as e:
            last_error = str(e)
            debug_print(f"TOTP secrets unavailable: {e}")
            if fetch_and_update_secrets():
                debug_print("TOTP secrets updated, retrying token refresh")
                retry += 1
                if retry < max_retries:
                    time.sleep(TOKEN_RETRY_TIMEOUT)
                continue
            raise RuntimeError(f"Failed to obtain TOTP secrets for token refresh: {e}")
        except Exception as e:
            last_error = str(e)
            debug_print(f"Token refresh attempt failed: {e}")
            retry += 1
            if retry < max_retries:
                time.sleep(TOKEN_RETRY_TIMEOUT)

    if retry == max_retries:

        if fetch_and_update_secrets():
            try:
                debug_print("Retrying token refresh after secrets update")
                token_data = refresh_access_token_from_sp_dc(sp_dc)
                token = token_data["access_token"]
                client_id = token_data.get("client_id", "")
                length = token_data["length"]

                SP_CACHED_ACCESS_TOKEN = token
                SP_ACCESS_TOKEN_EXPIRES_AT = token_data["expires_at"]
                SP_CACHED_CLIENT_ID = client_id

                if SP_CACHED_ACCESS_TOKEN and check_token_validity(SP_CACHED_ACCESS_TOKEN, SP_CACHED_CLIENT_ID, USER_AGENT):
                    debug_print("Spotify access token obtained successfully after secrets update")
                    return SP_CACHED_ACCESS_TOKEN
            except Exception as e:
                last_error = str(e)
                debug_print(f"Token refresh after secrets update failed: {e}")

        error_msg = f"Failed to obtain a valid Spotify access token after {max_retries} attempts"
        if last_error:
            error_msg += f": {last_error}"
        raise RuntimeError(error_msg)

    return SP_CACHED_ACCESS_TOKEN


# -------------------------------------------------------
# Supporting functions when token source is set to client
# -------------------------------------------------------

# Returns random Spotify client user agent string
def get_random_spotify_user_agent() -> str:
    os_choice = random.choice(['windows', 'mac', 'linux'])

    if os_choice == 'windows':
        build = random.randint(120000000, 130000000)
        arch = random.choice(['Win32', 'Win32_x86_64'])
        device = random.choice(['desktop', 'laptop'])
        return f"Spotify/{build} {arch}/0 (PC {device})"

    elif os_choice == 'mac':
        build = random.randint(120000000, 130000000)
        arch = random.choice(['OSX_ARM64', 'OSX_X86_64'])
        major = random.randint(10, 15)
        minor = random.randint(0, 7)
        patch = random.randint(0, 5)
        os_version = f"OS X {major}.{minor}.{patch}"
        if arch == 'OSX_ARM64':
            bracket = f"[arm {random.randint(1, 3)}]"
        else:
            bracket = "[x86_64]"
        return f"Spotify/{build} {arch}/{os_version} {bracket}"

    else:  # linux
        build = random.randint(120000000, 130000000)
        arch = random.choice(['Linux; x86_64', 'Linux; x86'])
        return f"Spotify/{build} ({arch})"


# Encodes an integer using Protobuf varint format
def encode_varint(value):
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value //= 128
    result.append(value)
    return bytes(result)


# Encodes a string field with the given tag
def encode_string_field(tag, value):
    key = encode_varint((tag << 3) | 2)  # wire type 2 (length-delimited)
    value_bytes = value.encode('utf-8')
    length = encode_varint(len(value_bytes))
    return key + length + value_bytes


# Encodes a nested message field with the given tag
def encode_nested_field(tag, nested_bytes):
    key = encode_varint((tag << 3) | 2)
    length = encode_varint(len(nested_bytes))
    return key + length + nested_bytes


# Builds the Spotify Protobuf login request body
def build_spotify_auth_protobuf(device_id, system_id, user_uri_id, refresh_token):
    """
    {
      1: {
           1: "device_id",
           2: "system_id"
         },
      100: {
           1: "user_uri_id",
           2: "refresh_token"
         }
    }
    """
    device_info_msg = encode_string_field(1, device_id) + encode_string_field(2, system_id)
    field_device_info = encode_nested_field(1, device_info_msg)

    user_auth_msg = encode_string_field(1, user_uri_id) + encode_string_field(2, refresh_token)
    field_user_auth = encode_nested_field(100, user_auth_msg)

    return field_device_info + field_user_auth


# Reads a varint from data starting at index
def read_varint(data, index):
    shift = 0
    result = 0
    bytes_read = 0
    while True:
        b = data[index]
        result |= ((b & 0x7F) << shift)
        bytes_read += 1
        index += 1
        if not (b & 0x80):
            break
        shift += 7
    return result, bytes_read


# Parses Spotify Protobuf login response
def parse_protobuf_message(data):
    index = 0
    result = {}
    while index < len(data):
        try:
            key, key_len = read_varint(data, index)
        except IndexError:
            break
        index += key_len
        tag = key >> 3
        wire_type = key & 0x07
        if wire_type == 2:  # length-delimited
            length, len_len = read_varint(data, index)
            index += len_len
            raw_value = data[index:index + length]
            index += length
            # If the first byte is a control character (e.g. 0x0A) assume nested
            if raw_value and raw_value[0] < 0x20:
                value = parse_protobuf_message(raw_value)
            else:
                try:
                    value = raw_value.decode('utf-8')
                except UnicodeDecodeError:
                    value = raw_value
            result[tag] = value
        elif wire_type == 0:  # varint
            value, var_len = read_varint(data, index)
            index += var_len
            result[tag] = value
        else:
            break
    return result  # dictionary mapping tags to values


# Parses the Protobuf-encoded login request body file (as dumped for example by Proxyman) and returns a tuple:
# (device_id, system_id, user_uri_id, refresh_token)
def parse_login_request_body_file(file_path):
    """
    {
      1: {
           1: "device_id",
           2: "system_id"
         },
      100: {
           1: "user_uri_id",
           2: "refresh_token"
         }
    }
    """
    with open(file_path, "rb") as f:
        data = f.read()
    parsed = parse_protobuf_message(data)

    device_id = None
    system_id = None
    user_uri_id = None
    refresh_token = None

    if 1 in parsed:
        device_info = parsed[1]
        if isinstance(device_info, dict):
            device_id = device_info.get(1)
            system_id = device_info.get(2)
        else:
            pass

    if 100 in parsed:
        user_auth = parsed[100]
        if isinstance(user_auth, dict):
            user_uri_id = user_auth.get(1)
            refresh_token = user_auth.get(2)

    protobuf_fields = {
        "device_id": device_id,
        "system_id": system_id,
        "user_uri_id": user_uri_id,
        "refresh_token": refresh_token,
    }

    protobuf_missing_fields = [name for name, value in protobuf_fields.items() if value is None]

    if protobuf_missing_fields:
        missing_str = ", ".join(protobuf_missing_fields)
        raise Exception(f"Following fields could not be extracted: {missing_str}")

    return device_id, system_id, user_uri_id, refresh_token


# Recursively flattens nested dictionaries or lists into a single string
def deep_flatten(value):
    if isinstance(value, dict):
        return "".join(deep_flatten(v) for k, v in sorted(value.items()))
    elif isinstance(value, list):
        return "".join(deep_flatten(item) for item in value)
    else:
        return str(value)


# Returns the input if it's a dict, parses as Protobuf it if it's bytes or returns an empty dict otherwise
def ensure_dict(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, (bytes, bytearray)):
        try:
            return parse_protobuf_message(value)
        except Exception:
            return {}
    return {}


# Parses the Protobuf-encoded client token request body file (as dumped for example by Proxyman) and returns a tuple:
# (app_version, device_id, system_id, cpu_arch, os_build, platform, os_major, os_minor, client_model)
def parse_clienttoken_request_body_file(file_path):
    """
        1: 1 (const)
        2: {
          1: "app_version"
          2: "device_id"
          3: {
            1: {
              4: {
                1: "cpu_arch"
                3: "os_build"
                4: "platform"
                5: "os_major"
                6: "os_minor"
                8: "client_model"
              }
            }
            2: "system_id"
          }
        }
    """

    with open(file_path, "rb") as f:
        data = f.read()

    root = ensure_dict(parse_protobuf_message(data).get(2))

    app_version = root.get(1)
    device_id = root.get(2)

    nested_3 = ensure_dict(root.get(3))
    nested_1 = ensure_dict(nested_3.get(1))
    nested_4 = ensure_dict(nested_1.get(4))

    cpu_arch = nested_4.get(1)
    os_build = nested_4.get(3)
    platform = nested_4.get(4)
    os_major = nested_4.get(5)
    os_minor = nested_4.get(6)
    client_model = nested_4.get(8)

    system_id = nested_3.get(2)

    required = {
        "app_version": app_version,
        "device_id": device_id,
        "system_id": system_id,
    }
    missing = [k for k, v in required.items() if v is None]
    if missing:
        raise Exception(f"Could not extract fields: {', '.join(missing)}")

    return (app_version, device_id, system_id, cpu_arch, os_build, platform, os_major, os_minor, client_model)


# Converts Spotify user agent string to Protobuf app_version string
# For example: 'Spotify/126200580 Win32_x86_64/0 (PC desktop)' to '1.2.62.580.g<random-hex>'
def ua_to_app_version(user_agent: str) -> str:

    m = re.search(r"Spotify/(\d{5,})", user_agent)
    if not m:
        raise ValueError(f"User-Agent missing build number: {user_agent!r}")

    digits = m.group(1)
    if len(digits) < 5:
        raise ValueError(f"Build number too short: {digits}")

    major = digits[0]
    minor = digits[1]
    patch = str(int(digits[2:4]))
    build = str(int(digits[4:]))
    suffix = secrets.token_hex(4)

    return f"{major}.{minor}.{patch}.{build}.g{suffix}"


# Builds the Protobuf client token request body
def build_clienttoken_request_protobuf(app_version, device_id, system_id, cpu_arch=10, os_build=19045, platform=2, os_major=9, os_minor=9, client_model=34404):
    """
        1: 1 (const)
        2: {
          1: "app_version"
          2: "device_id"
          3: {
            1: {
              4: {
                1: "cpu_arch"
                3: "os_build"
                4: "platform"
                5: "os_major"
                6: "os_minor"
                8: "client_model"
              }
            }
            2: "system_id"
          }
        }
    """

    leaf = (
        encode_varint((1 << 3) | 0) + encode_varint(cpu_arch) + encode_varint((3 << 3) | 0) + encode_varint(os_build) + encode_varint((4 << 3) | 0) + encode_varint(platform) + encode_varint((5 << 3) | 0) + encode_varint(os_major) + encode_varint((6 << 3) | 0) + encode_varint(os_minor) + encode_varint((8 << 3) | 0) + encode_varint(client_model))

    msg_4 = encode_nested_field(4, leaf)
    msg_1 = encode_nested_field(1, msg_4)
    msg_3 = msg_1 + encode_string_field(2, system_id)

    payload = (encode_string_field(1, app_version) + encode_string_field(2, device_id) + encode_nested_field(3, msg_3))

    root = (encode_varint((1 << 3) | 0) + encode_varint(1) + encode_nested_field(2, payload))

    return root


# Fetches Spotify access token based on provided device_id, system_id, user_uri_id, refresh_token and client_token value
def spotify_get_access_token_from_client(device_id, system_id, user_uri_id, refresh_token, client_token):
    global SP_CACHED_ACCESS_TOKEN, SP_CACHED_REFRESH_TOKEN, SP_ACCESS_TOKEN_EXPIRES_AT

    if SP_CACHED_ACCESS_TOKEN and time.time() < SP_ACCESS_TOKEN_EXPIRES_AT and check_token_validity(SP_CACHED_ACCESS_TOKEN, user_agent=USER_AGENT):
        debug_print("Using cached Spotify access token (client source)")
        return SP_CACHED_ACCESS_TOKEN

    if not client_token:
        raise Exception("Client token is missing")

    if SP_CACHED_REFRESH_TOKEN:
        debug_print("Using cached refresh token for client auth flow")
        refresh_token = SP_CACHED_REFRESH_TOKEN

    protobuf_body = build_spotify_auth_protobuf(device_id, system_id, user_uri_id, refresh_token)

    parsed_url = urlparse(LOGIN_URL)
    host = parsed_url.netloc
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "Content-Type": "application/x-protobuf",
        "User-Agent": USER_AGENT,
        "X-Retry-Count": "0",
        "Client-Token": client_token,
        "Origin": origin,
        "Accept-Language": "en-Latn-GB,en-GB;q=0.9,en;q=0.8",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }

    try:
        if platform.system() != 'Windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(FUNCTION_TIMEOUT + 2)
        debug_print(f"HTTP POST {LOGIN_URL} [client auth] headers={sanitize_debug_headers(headers)} payload_len={len(protobuf_body)}")
        response = req.post(LOGIN_URL, headers=headers, data=protobuf_body, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        debug_print(f"HTTP POST {LOGIN_URL} [client auth] -> {response.status_code}")
    except TimeoutException as e:
        debug_print(f"HTTP POST {LOGIN_URL} [client auth] timeout: {e}")
        raise Exception(f"spotify_get_access_token_from_client() network request timeout after {display_time(FUNCTION_TIMEOUT + 2)}: {e}")
    except Exception as e:
        debug_print(f"HTTP POST {LOGIN_URL} [client auth] failed: {e}")
        raise Exception(f"spotify_get_access_token_from_client() network request error: {e}")
    finally:
        if platform.system() != 'Windows':
            signal.alarm(0)

    if response.status_code != 200:
        if response.headers.get("client-token-error") == "INVALID_CLIENTTOKEN":
            raise Exception(f"Request failed with status {response.status_code}: invalid client token")
        elif response.headers.get("client-token-error") == "EXPIRED_CLIENTTOKEN":
            raise Exception(f"Request failed with status {response.status_code}: expired client token")

        try:
            error_json = response.json()
        except ValueError:
            error_json = {}

        if error_json.get("error") == "invalid_grant":
            desc = error_json.get("error_description", "")
            if "refresh token" in desc.lower() and "revoked" in desc.lower():
                raise Exception(f"Request failed with status {response.status_code}: refresh token has been revoked")
            elif "refresh token" in desc.lower() and "expired" in desc.lower():
                raise Exception(f"Request failed with status {response.status_code}: refresh token has expired")
            elif "invalid refresh token" in desc.lower():
                raise Exception(f"Request failed with status {response.status_code}: refresh token is invalid")
            else:
                raise Exception(f"Request failed with status {response.status_code}: invalid grant during refresh ({desc})")

        raise Exception(f"Request failed with status code {response.status_code}\nResponse Headers: {response.headers}\nResponse Content (raw): {response.content}\nResponse text: {response.text}")

    parsed = parse_protobuf_message(response.content)
    # {1: {1: user_uri_id, 2: access_token, 3: refresh_token, 4: expires_in}}
    access_token_raw = None
    expires_in = 3600  # default
    if 1 in parsed and isinstance(parsed[1], dict):
        nested = parsed[1]
        access_token_raw = nested.get(2)
        user_uri_id = parsed[1].get(1)

        if 4 in nested:
            raw_expires = nested.get(4)
            if isinstance(raw_expires, (int, str, bytes)):
                try:
                    expires_in = int(raw_expires)
                except ValueError:
                    expires_in = 3600

    access_token = deep_flatten(access_token_raw) if access_token_raw else None

    if not access_token:
        raise Exception("Access token not found in response")

    SP_CACHED_ACCESS_TOKEN = access_token
    SP_CACHED_REFRESH_TOKEN = parsed[1].get(3)
    SP_ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in
    return access_token


# Fetches fresh client token
def spotify_get_client_token(app_version, device_id, system_id, **device_overrides):
    global SP_CACHED_CLIENT_TOKEN, SP_CLIENT_TOKEN_EXPIRES_AT

    if SP_CACHED_CLIENT_TOKEN and time.time() < SP_CLIENT_TOKEN_EXPIRES_AT:
        debug_print("Using cached client token")
        return SP_CACHED_CLIENT_TOKEN

    body = build_clienttoken_request_protobuf(app_version, device_id, system_id, **device_overrides)

    headers = {
        "Host": "clienttoken.spotify.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Accept": "application/x-protobuf",
        "Content-Type": "application/x-protobuf",
        "User-Agent": USER_AGENT,
        "Origin": "https://clienttoken.spotify.com",
        "Accept-Language": "en-Latn-GB,en-GB;q=0.9,en;q=0.8",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }

    try:
        if platform.system() != 'Windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(FUNCTION_TIMEOUT + 2)
        debug_print(f"HTTP POST {CLIENTTOKEN_URL} [client token] app_version={app_version}, device_overrides={device_overrides}, payload_len={len(body)}")
        response = req.post(CLIENTTOKEN_URL, headers=headers, data=body, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        debug_print(f"HTTP POST {CLIENTTOKEN_URL} [client token] -> {response.status_code}")
    except TimeoutException as e:
        debug_print(f"HTTP POST {CLIENTTOKEN_URL} [client token] timeout: {e}")
        raise Exception(f"spotify_get_client_token() network request timeout after {display_time(FUNCTION_TIMEOUT + 2)}: {e}")
    except Exception as e:
        debug_print(f"HTTP POST {CLIENTTOKEN_URL} [client token] failed: {e}")
        raise Exception(f"spotify_get_client_token() network request error: {e}")
    finally:
        if platform.system() != 'Windows':
            signal.alarm(0)

    if response.status_code != 200:
        raise Exception(f"clienttoken request failed - status {response.status_code}\nHeaders: {response.headers}\nBody (raw): {response.content[:120]}...")

    parsed = parse_protobuf_message(response.content)
    inner = parsed.get(2, {})
    client_token = deep_flatten(inner.get(1)) if inner.get(1) else None
    ttl = int(inner.get(3, 0)) or 1209600

    if not client_token:
        raise Exception("clienttoken response did not contain a token")

    SP_CACHED_CLIENT_TOKEN = client_token
    SP_CLIENT_TOKEN_EXPIRES_AT = time.time() + ttl
    debug_print(f"Client token refreshed successfully, ttl={ttl}s")

    return client_token


# Fetches Spotify access token with automatic client token refresh
def spotify_get_access_token_from_client_auto(device_id, system_id, user_uri_id, refresh_token):
    client_token = None

    if all([
        CLIENTTOKEN_URL,
        APP_VERSION,
        CPU_ARCH is not None and CPU_ARCH > 0,
        OS_BUILD is not None and OS_BUILD > 0,
        PLATFORM is not None and PLATFORM > 0,
        OS_MAJOR is not None and OS_MAJOR > 0,
        OS_MINOR is not None and OS_MINOR > 0,
        CLIENT_MODEL is not None and CLIENT_MODEL > 0
    ]):
        debug_print("Attempting to refresh/get client token before client auth")
        client_token = spotify_get_client_token(app_version=APP_VERSION, device_id=device_id, system_id=system_id, cpu_arch=CPU_ARCH, os_build=OS_BUILD, platform=PLATFORM, os_major=OS_MAJOR, os_minor=OS_MINOR, client_model=CLIENT_MODEL)

    try:
        return spotify_get_access_token_from_client(device_id, system_id, user_uri_id, refresh_token, client_token)
    except Exception as e:
        err = str(e).lower()
        debug_print(f"Client auth failed: {e}")
        if all([
            CLIENTTOKEN_URL,
            APP_VERSION,
            CPU_ARCH is not None and CPU_ARCH > 0,
            OS_BUILD is not None and OS_BUILD > 0,
            PLATFORM is not None and PLATFORM > 0,
            OS_MAJOR is not None and OS_MAJOR > 0,
            OS_MINOR is not None and OS_MINOR > 0,
            CLIENT_MODEL is not None and CLIENT_MODEL > 0
        ]) and ("invalid client token" in err or "expired client token" in err):
            global SP_CLIENT_TOKEN_EXPIRES_AT
            SP_CLIENT_TOKEN_EXPIRES_AT = 0
            debug_print("Client token invalid/expired, forcing refresh and retry")

            client_token = spotify_get_client_token(app_version=APP_VERSION, device_id=DEVICE_ID, system_id=SYSTEM_ID, cpu_arch=CPU_ARCH, os_build=OS_BUILD, platform=PLATFORM, os_major=OS_MAJOR, os_minor=OS_MINOR, client_model=CLIENT_MODEL)

            return spotify_get_access_token_from_client(device_id, system_id, user_uri_id, refresh_token, client_token)
        raise


# --------------------------------------------------------

# Fetches Spotify access token based on provided sp_client_id & sp_client_secret values (Client Credentials OAuth Flow)
def spotify_get_access_token_from_oauth_app(sp_client_id, sp_client_secret):
    global SP_CACHED_OAUTH_APP_TOKEN

    if not sp_client_id or not sp_client_secret:
        return None

    try:
        from spotipy.oauth2 import SpotifyClientCredentials
        from spotipy.cache_handler import CacheFileHandler, MemoryCacheHandler
    except ImportError:
        print("* Warning: the 'spotipy' package is required, install it with `pip install spotipy`")
        return None

    if SP_CACHED_OAUTH_APP_TOKEN and check_token_validity(SP_CACHED_OAUTH_APP_TOKEN, oauth_app=True):
        debug_print("Using cached OAuth app access token")
        return SP_CACHED_OAUTH_APP_TOKEN

    if SP_APP_TOKENS_FILE:
        cache_handler = CacheFileHandler(cache_path=SP_APP_TOKENS_FILE)
    else:
        cache_handler = MemoryCacheHandler()

    session = req.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    auth_manager = SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret, cache_handler=cache_handler, requests_session=session)  # type: ignore[arg-type]

    SP_CACHED_OAUTH_APP_TOKEN = auth_manager.get_access_token(as_dict=False)
    debug_print("OAuth app access token refreshed successfully")

    return SP_CACHED_OAUTH_APP_TOKEN


# Fetches list of Spotify friends
def spotify_get_friends_json(access_token):
    url = "https://guc-spclient.spotify.com/presence-view/v1/buddylist"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie":
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })

    debug_print(f"HTTP GET {url} [buddylist] headers={sanitize_debug_headers(headers)}")
    response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
    debug_print(f"HTTP GET {url} [buddylist] -> {response.status_code}")
    if response.status_code == 401:
        raise Exception("401 Unauthorized for url: " + url)
    response.raise_for_status()
    friends_json = response.json()
    error_str = friends_json.get("error")
    if error_str:
        raise ValueError(error_str)

    return friends_json


# Converts Spotify URI (e.g. spotify:user:username) to URL (e.g. https://open.spotify.com/user/username)
def spotify_convert_uri_to_url(uri):
    # add si parameter so link opens in native Spotify app after clicking
    si = "?si=1"
    # si=""

    uri = uri or ''
    url = ""
    if not isinstance(uri, str):
        return url
    if "spotify:user:" in uri:
        s_id = uri.split(':', 2)[2]
        url = f"https://open.spotify.com/user/{s_id}{si}"
    elif "spotify:artist:" in uri:
        s_id = uri.split(':', 2)[2]
        url = f"https://open.spotify.com/artist/{s_id}{si}"
    elif "spotify:track:" in uri:
        s_id = uri.split(':', 2)[2]
        url = f"https://open.spotify.com/track/{s_id}{si}"
    elif "spotify:album:" in uri:
        s_id = uri.split(':', 2)[2]
        url = f"https://open.spotify.com/album/{s_id}{si}"
    elif "spotify:playlist:" in uri:
        s_id = uri.split(':', 2)[2]
        url = f"https://open.spotify.com/playlist/{s_id}{si}"

    return url


# Returns list of Spotify friends
def spotify_list_friends(friend_activity):

    print(f"Number of friends:\t\t{len(friend_activity['friends'])}\n")

    for index, friend in enumerate(friend_activity["friends"]):
        sp_uri = friend["user"].get("uri").split("spotify:user:", 1)[1]
        sp_username = friend["user"].get("name")
        sp_artist = friend["track"]["artist"].get("name")
        sp_album = friend["track"]["album"].get("name")
        sp_playlist = friend["track"]["context"].get("name")
        sp_track = friend["track"].get("name")
        sp_ts = friend.get("timestamp")
        sp_album_uri = friend["track"]["album"].get("uri")
        sp_playlist_uri = friend["track"]["context"].get("uri")
        sp_track_uri = friend["track"].get("uri")

        sp_playlist_owner = ""
        if sp_playlist_uri:
            sp_accessToken_oauth_app = spotify_get_access_token_from_oauth_app(SP_APP_CLIENT_ID, SP_APP_CLIENT_SECRET)
            if sp_accessToken_oauth_app:
                sp_playlist_owner = spotify_get_playlist_owner(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
        playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""

        print("─" * HORIZONTAL_LINE)
        print(f"Username:\t\t\t{sp_username}")
        print(f"User URI ID:\t\t\t{sp_uri}")
        print(f"User URL:\t\t\t{spotify_convert_uri_to_url('spotify:user:' + sp_uri)}")
        print(f"\nLast played:\t\t\t{sp_artist} - {sp_track}\n")
        if 'spotify:playlist:' in sp_playlist_uri:
            print(f"Playlist:\t\t\t{sp_playlist}{playlist_suffix}")
        print(f"Album:\t\t\t\t{sp_album}")

#jmk    if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
        if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
            print(f"\nContext (Album):\t\t{sp_playlist}")

        if 'spotify:artist:' in sp_playlist_uri:
            print(f"\nContext (Artist):\t\t{sp_playlist}")

        print(f"\nTrack URL:\t\t\t{spotify_convert_uri_to_url(sp_track_uri)}")
        if 'spotify:playlist:' in sp_playlist_uri:
            print(f"Playlist URL:\t\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")
        print(f"Album URL:\t\t\t{spotify_convert_uri_to_url(sp_album_uri)}")

#jmk    if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
        if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
            print(f"Context (Album) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

        if 'spotify:artist:' in sp_playlist_uri:
            print(f"Context (Artist) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

        apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))

        music_urls_output = format_music_urls_console(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
        if music_urls_output:
            print(music_urls_output)
        lyrics_output = format_lyrics_urls_console(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
        if lyrics_output:
            print(lyrics_output)

        print(f"\nLast activity:\t\t\t{get_date_from_ts(float(str(sp_ts)[0:-3]))} ({calculate_timespan(int(time.time()), datetime.fromtimestamp(float(str(sp_ts)[0:-3])))} ago)")


# Returns information for specific Spotify friend's user URI id
def spotify_get_friend_info(friend_activity, uri):
    for friend in friend_activity["friends"]:
        sp_uri = friend["user"]["uri"].split("spotify:user:", 1)[1]
        if sp_uri == uri:
            sp_username = friend["user"].get("name")
            sp_artist = friend["track"]["artist"].get("name")
            sp_album = friend["track"]["album"].get("name")
            sp_album_uri = friend["track"]["album"].get("uri")
            sp_playlist = friend["track"]["context"].get("name")
            sp_playlist_uri = friend["track"]["context"].get("uri")
            sp_track = friend["track"].get("name")
            sp_track_uri = str(friend["track"].get("uri"))
            if "spotify:track:" in sp_track_uri:
                sp_track_uri_id = sp_track_uri.split(':', 2)[2]
            else:
                sp_track_uri_id = ""
            sp_ts = int(str(friend.get("timestamp"))[0:-3])
            return True, {"sp_uri": sp_uri, "sp_username": sp_username, "sp_artist": sp_artist, "sp_track": sp_track, "sp_track_uri": sp_track_uri, "sp_track_uri_id": sp_track_uri_id, "sp_album": sp_album, "sp_album_uri": sp_album_uri, "sp_playlist": sp_playlist, "sp_playlist_uri": sp_playlist_uri, "sp_ts": sp_ts}
    return False, {}


# Returns information for specific Spotify playlist URI
def spotify_get_playlist_owner(access_token, playlist_uri, oauth_app=False):
    if not access_token:
        raise Exception("spotify_get_playlist_owner(): access_token is empty")

    playlist_id = playlist_uri.split(':', 2)[2]

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields=name,owner"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie" and not oauth_app:
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })

    try:
        debug_print(f"HTTP GET {url} [playlist owner] headers={sanitize_debug_headers(headers)}")
        response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        debug_print(f"HTTP GET {url} [playlist owner] -> {response.status_code}")
        if response.status_code == 404:
            # Spotify-curated playlists often return 404 when accessed via Client Credentials Flow
            sp_playlist_owner = "Spotify"
        else:
            response.raise_for_status()
            json_response = response.json()

            sp_playlist_owner = json_response["owner"].get("display_name", "")
        return sp_playlist_owner
    except Exception as e:
        # print(e)
        print_to_log(e)
        return False
        # raise

# Returns information for specific Spotify playlist URI
def spotify_get_playlist_image_url(access_token, playlist_uri, oauth_app=False):
    if not access_token:
        raise Exception("spotify_get_playlist_owner(): access_token is empty")

    playlist_id = playlist_uri.split(':', 2)[2]

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields=name,images"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie" and not oauth_app:
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })

    try:
        response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        if response.status_code == 404:
            # Spotify-curated playlists often return 404 when accessed via Client Credentials Flow
            sp_playlist_image_url = get_spotify_playlist_image(playlist_id)
            if not sp_playlist_image_url:
                return False
        else:
            response.raise_for_status()
            json_response = response.json()

            sp_playlist_image_url = json_response["images"][0].get("url", "")
        return sp_playlist_image_url
    except Exception as e:
        # print(e)
        print_to_log(e)
        return False
        # raise


# Returns information for specific Spotify track URI
def spotify_get_track_info(access_token, track_uri, oauth_app=False):
    if not access_token:
        raise Exception("spotify_get_track_info(): access_token is empty")

    track_id = track_uri.split(':', 2)[2]
    url = "https://api.spotify.com/v1/tracks/" + track_id
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie" and not oauth_app:
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })
    # add si parameter so link opens in native Spotify app after clicking
    si = "?si=1"

    try:
        debug_print(f"HTTP GET {url} [track info] headers={sanitize_debug_headers(headers)}")
        response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        debug_print(f"HTTP GET {url} [track info] -> {response.status_code}")
        response.raise_for_status()
        json_response = response.json()
        sp_track_duration = int(json_response.get("duration_ms") / 1000)
        sp_track_url = json_response["external_urls"].get("spotify") + si
        sp_track_name = json_response.get("name")
        sp_artist_url = json_response["artists"][0]["external_urls"].get("spotify") + si
        sp_artist_name = json_response["artists"][0].get("name")
        sp_album_url = json_response["album"]["external_urls"].get("spotify") + si
        sp_album_name = json_response["album"].get("name")
        sp_album_image_url = json_response["album"]["images"][0].get("url", "")
        return {"sp_track_duration": sp_track_duration, "sp_track_url": sp_track_url, "sp_artist_url": sp_artist_url, "sp_album_url": sp_album_url, "sp_track_name": sp_track_name, "sp_artist_name": sp_artist_name, "sp_album_name": sp_album_name, "sp_album_image_url": sp_album_image_url}
    except Exception:
        raise


def get_spotify_playlist_image(playlist_id: str) -> str:
    url = f"https://open.spotify.com/playlist/{playlist_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = req.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    tag = soup.find("meta", {"property": "og:image"})
    if not tag or not tag.get("content"):
        return False

    return tag["content"]


# # Returns information for specific Spotify playlist URI
# def spotify_get_playlist_info(access_token, playlist_uri, oauth_app=False):
    # if not access_token:
        # raise Exception("spotify_get_playlist_info(): access_token is empty")

    # print_debug(f"spotify_get_playlist_info")
    # print_debug(f"access_token: {access_token}")
    # print_debug(f"oauth_app: {oauth_app}")
    # # return False
    
    # playlist_id = playlist_uri.split(':', 2)[2]
    
    # url = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields=name,owner,followers,external_urls,images"
    # headers = {
        # "Authorization": f"Bearer {access_token}",
        # "User-Agent": USER_AGENT
    # }

    # if TOKEN_SOURCE == "cookie" and not oauth_app:
        # headers.update({
            # "Client-Id": SP_CACHED_CLIENT_ID
        # })
    # # add si parameter so link opens in native Spotify app after clicking
    # si = "?si=1"

    # try:
        # response = SESSION.get(url, headers=headers, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        # print_debug(f"response: {response}")
        # if response.status_code != 404:
            # print_debug(f"json_response: {json_response}")
        # if response.status_code == 404:
            # sp_playlist_image_url = get_spotify_playlist_image(playlist_id)
            # if not sp_playlist_image_url:
                # return False
            # sp_playlist_owner = "Spotify"
        # else:
            # response.raise_for_status()
            # json_response = response.json()

            # # sp_playlist_name = json_response.get("name")
            # sp_playlist_owner = json_response["owner"].get("display_name", "")
            # # sp_playlist_owner_url = json_response["owner"]["external_urls"].get("spotify")
            # # sp_playlist_followers = int(json_response["followers"].get("total"))
            # # sp_playlist_url = json_response["external_urls"].get("spotify") + si
            # sp_playlist_image_url = json_response["images"][0].get("url", "")
        # return {"sp_playlist_owner": sp_playlist_owner, "sp_playlist_image_url": sp_playlist_image_url}
    # except Exception as e:
        # print(e)
        # raise

# Checks if a Spotify user URI ID has been deleted
def is_user_removed(access_token, user_uri_id, oauth_app=False):
    # Use internal Spotify API (official /users/{id} endpoint was removed in Feb 2026)
    url = f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{user_uri_id}?playlist_limit=0&artist_limit=0&episode_limit=0&market=from_token"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT
    }

    if TOKEN_SOURCE == "cookie" and not oauth_app:
        headers.update({
            "Client-Id": SP_CACHED_CLIENT_ID
        })

    if platform.system() != 'Windows':
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(FUNCTION_TIMEOUT + 2)

    try:
        temp_session = req.Session()
        temp_session.headers.update(headers)

        debug_print(f"HTTP GET {url} [user removed check] headers={sanitize_debug_headers(headers)}")
        response = temp_session.get(url, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
        debug_print(f"HTTP GET {url} [user removed check] -> {response.status_code}")

        if response.status_code == 429:
            return False

        if response.status_code == 404:
            return True
        return False
    except TimeoutException:
        return False
    except req.HTTPError as e:
        if e.response.status_code == 429:
            return False
        elif e.response.status_code == 404:
            return True
        return False
    except Exception:
        return False
    finally:
        if platform.system() != 'Windows':
            signal.alarm(0)


def spotify_macos_play_song(sp_track_uri_id, method=SPOTIFY_MACOS_PLAYING_METHOD):
    if method == "apple-script":   # apple-script
        script = f'tell app "Spotify" to play track "spotify:track:{sp_track_uri_id}"'
        proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = proc.communicate(script)
    else:                          # trigger-url - just trigger track URL in the client
        subprocess.call(('open', spotify_convert_uri_to_url(f"spotify:track:{sp_track_uri_id}")))


def spotify_macos_play_pause(action, method=SPOTIFY_MACOS_PLAYING_METHOD):
    if method == "apple-script":   # apple-script
        if str(action).lower() == "pause":
            script = 'tell app "Spotify" to pause'
            proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = proc.communicate(script)
        elif str(action).lower() == "play":
            script = 'tell app "Spotify" to play'
            proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = proc.communicate(script)


def spotify_linux_play_song(sp_track_uri_id, method=SPOTIFY_LINUX_PLAYING_METHOD):
    if method == "dbus-send":      # dbus-send
        subprocess.call((f"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:'spotify:track:{sp_track_uri_id}'"), shell=True)
    elif method == "qdbus":        # qdbus
        subprocess.call((f"qdbus org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri spotify:track:{sp_track_uri_id}"), shell=True)
    else:                          # trigger-url - just trigger track URL in the client
        subprocess.call(('xdg-open', spotify_convert_uri_to_url(f"spotify:track:{sp_track_uri_id}")), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def spotify_linux_play_pause(action, method=SPOTIFY_LINUX_PLAYING_METHOD):
    if method == "dbus-send":      # dbus-send
        if str(action).lower() == "pause":
            subprocess.call((f"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause"), shell=True)
        elif str(action).lower() == "play":
            subprocess.call((f"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play"), shell=True)
    elif method == "qdbus":        # qdbus
        if str(action).lower() == "pause":
            subprocess.call((f"qdbus org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause"), shell=True)
        elif str(action).lower() == "play":
            subprocess.call((f"qdbus org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play"), shell=True)


def spotify_win_play_song(sp_track_uri_id, method=SPOTIFY_WINDOWS_PLAYING_METHOD):
    WIN_SPOTIFY_APP_PATH = r'%APPDATA%\Spotify\Spotify.exe'

    if method == "start-uri":      # start-uri
        subprocess.call((f"start spotify:track:{sp_track_uri_id}"), shell=True)
    elif method == "spotify-cmd":  # spotify-cmd
        subprocess.call((f"{WIN_SPOTIFY_APP_PATH} --uri=spotify:track:{sp_track_uri_id}"), shell=True)
    else:                          # trigger-url - just trigger track URL in the client
        os.startfile(spotify_convert_uri_to_url(f"spotify:track:{sp_track_uri_id}"))


# Finds an optional config file
def find_config_file(cli_path=None):
    """
    Search for an optional config file in:
      1) CLI-provided path (must exist if given)
      2) ./{DEFAULT_CONFIG_FILENAME}
      3) ~/.{DEFAULT_CONFIG_FILENAME}
      4) script-directory/{DEFAULT_CONFIG_FILENAME}
    """

    if cli_path:
        p = Path(os.path.expanduser(cli_path))
        return str(p) if p.is_file() else None

    candidates = [
        Path.cwd() / DEFAULT_CONFIG_FILENAME,
        Path.home() / f".{DEFAULT_CONFIG_FILENAME}",
        Path(__file__).parent / DEFAULT_CONFIG_FILENAME,
    ]

    for p in candidates:
        if p.is_file():
            return str(p)
    return None


# Resolves an executable path by checking if it's a valid file or searching in $PATH
def resolve_executable(path):
    if os.path.isfile(path) and os.access(path, os.X_OK):
        return path

    found = shutil.which(path)
    if found:
        return found

    raise FileNotFoundError(f"Could not find executable '{path}'")


def notify_playlist_detected(notify_playlist, songstr, timediff, track, artist, album):
    dz_msg_screen = f"{timestring()}: {ERR_CODE}, [{timediff}] *** Playlist '{notify_playlist['name']}' Detected"
    if notify_playlist.get('notify', NOTIFY_PLAYLIST_DETECTED):
        update_spreadsheet_row(f"----------------- {notify_playlist['name']} Detected -----", False)
        send_email(f"{GMAIL_TAG}----------------- {notify_playlist['name']} Detected -----", "  ", "  ", SMTP_SSL)
        if SEND_NOTIFY:
            dz_message = f"*** Playlist '{notify_playlist['name']}' Detected: {songstr}"
            # send_notification(dz_message)
            send_notification(dz_message, "", track, artist, album, notify_playlist['name'], "", 0)
    return dz_msg_screen


def notify_playlist_cleared(notify_playlist, songstr, timediff, track, artist, album):
    dz_message = f"*** Playlist '{notify_playlist['name']}' Cleared: {songstr} - Song Count: {notify_playlist['count_start']}"
    dz_msg_screen = f"{timestring()}: {ERR_CODE}, [{timediff}] *** Playlist '{notify_playlist['name']}' Cleared, Song Count: {notify_playlist['count_start']}"
    if notify_playlist.get('notify', NOTIFY_PLAYLIST_DETECTED):
        update_spreadsheet_row(f"----------------- {notify_playlist['name']} Cleared -----", False)
        send_email(f"{GMAIL_TAG}----------------- {notify_playlist['name']} Cleared -----", "  ", "  ", SMTP_SSL)
        if SEND_NOTIFY:
            # send_notification(dz_message)
            send_notification(dz_message, "", track, artist, album, notify_playlist['name'], "", notify_playlist['count_start'])
    return dz_message, dz_msg_screen
#send_notification(f"END: [{time_diff_str()}]: {songstring()}, Song Count: {listened_songs}", sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '', time_diff_str(), listened_songs)
#def send_notification(message, image_url="", track="", artist="", album="", playlist="", timediffstr="", count=0):

def monitored_playlist_detected(detected_playlist, songstr, timediff, print_msg, track="", artist="", album=""):
    msg = build_dz_string(detected_playlist)
    if DEBUG_JMK:
        msg = msg + " (1)"
    dz_msg_screen = notify_playlist_detected(detected_playlist, songstr, timediff, track, artist, album)
    if print_msg:
        print_to_both(dz_msg_screen)
        dz_msg_screen = ""

    # body_dz      = msg + "\n"
    # body_dz_html = msg + "<br>"

    return msg + "\n", msg + "<br>", msg, dz_msg_screen


def monitored_playlist_cleared(cleared_playlist, songstr, timediff, track="", artist="", album=""):
    dz_message, dz_msg_screen = notify_playlist_cleared(cleared_playlist, songstr, timediff, track, artist, album)
    # if found_playlist['name'] == DZ_PLAYLIST_NAME:
        # dz_message, dz_msg_screen = notify_playlist_cleared(cleared_playlist)
    # else:
        # dz_message    = f"*** {detected_playlist['name']} Cleared: {songstring()}, Song Count: {notify_playlist['count_start']}"
        # dz_msg_screen = f"{timestring()}: {ERR_CODE}, [{timediff()}] {dz_message}"

    return dz_message, dz_msg_screen


# Monitors music activity of the specified Spotify friend's user URI ID
def spotify_monitor_friend_uri(user_uri_id, tracks, csv_file_name):
    global SP_CACHED_ACCESS_TOKEN
    global count_overridden
   
    sp_active_ts_start = 0
    sp_active_ts_stop = 0
    sp_active_ts_start_old = 0
    user_not_found = False
    listened_songs = 0
    listened_songs_old = 0
    looped_songs = 0
    looped_songs_old = 0
    skipped_songs = 0
    skipped_songs_old = 0
    sp_artist_old = ""
    sp_track_old = ""
    song_on_loop = 0
    recent_songs_session = []
    error_500_counter = 0
    error_500_start_ts = 0
    error_network_issue_counter = 0
    error_network_issue_start_ts = 0
    sp_accessToken = ""
    sp_accessToken_oauth_app = ""

    jmk_send = False
    found_playlist = False
    last_found_playlist = False
    active_ever = False
    icon_add = False
    hasTrack = False
    sp_playlist_owner = ""
    sp_playlist_image_url = ""
    playlist_suffix = ""
    
    def iconstring():
        nonlocal icon_add, playlist_suffix 
        return playlist_suffix + (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")
        
    def songstring():
        if sp_playlist and is_playlist:
            return f"{sp_track.strip()} - {sp_artist.strip()} ({sp_album.strip()}) [{sp_playlist.strip()}]{iconstring()}"
        else:
            return f"{sp_track.strip()} - {sp_artist.strip()} ({sp_album.strip()})"

    def songstringtext():
        return f"{sp_track} - {sp_artist} ({sp_album})"

    def time_diff_str():
        return str(round((sp_ts - sp_active_ts_start) / 60)).zfill(2)

    def reset_playlist_counts(playlist_name_to_protect=""):
        nonlocal icon_add
        nonlocal dz_message, body_dz, body_dz_html, dz_msg_screen
        
        if ALT_VIEW:
            icon_add = False
        if playlist_name_to_protect:
            print_debug(f"CLEARING ALL PLAYLIST COUNTS/STRINGS, BUT PROTECTING PLAYLIST START CNT -> {playlist_name_to_protect}")
        else:
            print_debug(f"CLEARING ALL PLAYLIST COUNTS/STRINGS, BUT NO PLAYLIST PROTECTION")
        dz_message = ""
        dz_msg_screen = ""
        body_dz = ""
        body_dz_html = ""
        for playlist_name, playlist_data in monitored_playlists_data.items():
            print_debug(f"-- CHECKING PLAYLIST {playlist_name}")
            if (playlist_name == playlist_name_to_protect):
                # playlist_data['count_start'] = 0
                playlist_data['count_end'] = 0
                # playlist_data['count_shuffle'] = 0
                print_debug(f"-- PROTECTED PLAYLIST COUNTS (start: {playlist_data['count_start']}, end: {playlist_data['count_end']}, shuffle: {playlist_data['count_shuffle']}) -> {playlist_name}")
            else:
                playlist_data['count_start'] = 0
                playlist_data['count_end'] = 0
                playlist_data['count_shuffle'] = 0
                print_debug(f"-- UNPROTECTED PLAYLIST COUNTS (start: {playlist_data['count_start']}, end: {playlist_data['count_end']}, shuffle: {playlist_data['count_shuffle']}) -> {playlist_name}")

    try:
        if csv_file_name:
            init_csv_file(csv_file_name)
    except Exception as e:
        print(f"* Error: {e}")

    email_sent = False

    out = f"Monitoring user {user_uri_id}"
    print(out)
    # print("─" * len(out))
    print("─" * HORIZONTAL_LINE)

    tracks_upper = {t.upper() for t in tracks}

    # Start loop
    while True:
        debug_print(f"Loop tick: token_source={TOKEN_SOURCE}, check_interval={SPOTIFY_CHECK_INTERVAL}, error_interval={SPOTIFY_ERROR_INTERVAL}")

        # Sometimes Spotify network functions halt even though we specified the timeout
        # To overcome this we use alarm signal functionality to kill it inevitably, not available on Windows
        if platform.system() != 'Windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(ALARM_TIMEOUT)
        try:
            if TOKEN_SOURCE == "client":
                sp_accessToken = spotify_get_access_token_from_client_auto(DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN)
            else:
                sp_accessToken = spotify_get_access_token_from_sp_dc(SP_DC_COOKIE)

            sp_accessToken_oauth_app = spotify_get_access_token_from_oauth_app(SP_APP_CLIENT_ID, SP_APP_CLIENT_SECRET)

            sp_friends = spotify_get_friends_json(sp_accessToken)
            sp_found, sp_data = spotify_get_friend_info(sp_friends, user_uri_id)
            debug_print(f"Friend lookup result: found={sp_found}")
            email_sent = False
            if platform.system() != 'Windows':
                signal.alarm(0)
        except TimeoutException:
            if platform.system() != 'Windows':
                signal.alarm(0)
            print(f"spotify_*() function timeout after {display_time(ALARM_TIMEOUT)}, retrying in {display_time(ALARM_RETRY)}")
            print_cur_ts("Timestamp:\t\t\t")
            time.sleep(ALARM_RETRY)
            continue
        except Exception as e:
            if platform.system() != 'Windows':
                signal.alarm(0)

            err = str(e).lower()
            debug_print(f"Main monitor loop error: {e}")

            print(f"* Error, retrying in {display_time(SPOTIFY_ERROR_INTERVAL)}: {e}")

            if TOKEN_SOURCE == 'cookie' and '401' in err:
                SP_CACHED_ACCESS_TOKEN = None

            client_errs = ['access token', 'invalid client token', 'expired client token', 'refresh token has been revoked', 'refresh token has expired', 'refresh token is invalid', 'invalid grant during refresh']
            cookie_errs = ['access token', 'unauthorized', 'unsuccessful token request']

            if TOKEN_SOURCE == 'client' and any(k in err for k in client_errs):
                print(f"* Error: client or refresh token may be invalid or expired!")
                if ERROR_NOTIFICATION and not email_sent:
                    m_subject = f"spotify_monitor: client or refresh token may be invalid or expired! (uri: {user_uri_id})"
                    m_body = f"Client or refresh token may be invalid or expired!\n{e}{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                    m_body_html = f"<html><head></head><body>Client or refresh token may be invalid or expired!<br>{escape(str(e))}{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                    print(f"Sending email notification to {RECEIVER_EMAIL}")
                    send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                    email_sent = True

            elif TOKEN_SOURCE == 'cookie' and any(k in err for k in cookie_errs):
                print(f"* Error: sp_dc may be invalid/expired or Spotify has broken sth again!")
                if ERROR_NOTIFICATION and not email_sent:
                    m_subject = f"spotify_monitor: sp_dc may be invalid/expired or Spotify has broken sth again! (uri: {user_uri_id})"
                    m_body = f"sp_dc may be invalid/expired or Spotify has broken sth again!\n{e}{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                    m_body_html = f"<html><head></head><body>sp_dc may be invalid/expired or Spotify has broken sth again!<br>{escape(str(e))}{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                    print(f"Sending email notification to {RECEIVER_EMAIL}")
                    send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                    email_sent = True

            print_cur_ts("Timestamp:\t\t\t")
            time.sleep(SPOTIFY_ERROR_INTERVAL)
            continue

        playlist_m_body = ""
        playlist_m_body_html = ""
        played_for_m_body = ""
        played_for_m_body_html = ""
        is_playlist = False
        playlist_suffix = ""

        # User is found in the Spotify's friend list just after starting the tool
        if sp_found:
            user_not_found = False

            sp_track_uri = sp_data["sp_track_uri"]
            sp_track_uri_id = sp_data["sp_track_uri_id"]
            sp_album_uri = sp_data["sp_album_uri"]
            sp_playlist_uri = sp_data["sp_playlist_uri"]

            # sp_playlist_data = {}
            try:
                sp_track_data = spotify_get_track_info(sp_accessToken_oauth_app, sp_track_uri, oauth_app=True)
                is_playlist = 'spotify:playlist:' in sp_playlist_uri
                if is_playlist:
                    sp_playlist_owner = spotify_get_playlist_owner(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                    sp_playlist_image_url = spotify_get_playlist_image_url(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                    playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""
                    playlist_suffix += (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")
            except Exception as e:
                print(f"* Error, retrying in {display_time(SPOTIFY_ERROR_INTERVAL)}: {e}")
                print_cur_ts("Timestamp:\t\t\t")
                time.sleep(SPOTIFY_ERROR_INTERVAL)
                continue

            sp_username = sp_data["sp_username"]

            sp_artist = sp_data["sp_artist"]
            if not sp_artist:
                sp_artist = sp_track_data["sp_artist_name"]

            sp_track = sp_data["sp_track"]
            if not sp_track:
                sp_track = sp_track_data["sp_track_name"]

            sp_playlist = sp_data["sp_playlist"]
            if JMK_MODE:
                if sp_playlist == "Discovery zone":
                    sp_playlist = "Discovery Zone"
            sp_album = sp_data["sp_album"]
            if not sp_album:
                sp_album = sp_track_data["sp_album_name"]

            sp_album_image_url = sp_track_data["sp_album_image_url"]
            if not sp_album_image_url:
                sp_album_image_url = ""

            sp_ts = sp_data["sp_ts"]
            cur_ts = int(time.time())

            sp_track_duration = sp_track_data["sp_track_duration"]
            sp_track_url = sp_track_data["sp_track_url"]
            sp_artist_url = sp_track_data["sp_artist_url"]
            sp_album_url = sp_track_data["sp_album_url"]

            sp_playlist_url = ""
            if is_playlist:
                sp_playlist_url = spotify_convert_uri_to_url(sp_playlist_uri)
                playlist_m_body = f"\nPlaylist: {sp_playlist}{playlist_suffix}"
                playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}{playlist_suffix}</a>"
                sp_playlist_owner = spotify_get_playlist_owner(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                sp_playlist_image_url = spotify_get_playlist_image_url(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""
                playlist_suffix += (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")
                # sp_playlist_image_url = sp_playlist_data.get("sp_playlist_image_url", "")
                # sp_playlist_owner = sp_playlist_data.get("sp_playlist_owner")

                if JMK_MODE:
                    hasTrack = (sp_playlist_owner == "Spotify") or (search_playlist(sp_accessToken_oauth_app, sp_playlist, sp_playlist_uri, sp_track_uri_id, sp_track, sp_artist, False))
                    print_debug(f"hasTrack (A1): {hasTrack}, sp_playlist_owner: {sp_playlist_owner}, sp_playlist: {sp_playlist}")
                    if hasTrack:
                        for playlist_data in monitored_playlists_data.values():
                            if sp_playlist and (sp_playlist.upper() == playlist_data.get('name', "B").upper()):
                                hasTrack = False
                                print_debug(f"hastrack Playlist Match (A2a): hastrack = FALSE, sp_playlist: {sp_playlist}")
                        print_debug(f"hasTrack (A2b): {hasTrack}, sp_playlist: {sp_playlist}")
                    
                    print_debug(f"hasTrack (A3): {hasTrack}, sp_playlist_owner: {sp_playlist_owner}")

                    # if hasTrack:
                        # print_debug(f"*** Track [{sp_track}] was found in playlist [{sp_playlist}{iconstring()}]")
                    if not hasTrack:
                        if (sp_playlist_owner != "Spotify"):
                            print_debug(f"SONG NOT IN REPORTED PLAYLIST (1)")
                            print_to_log(f"*** ERROR: track [{sp_track}] NOT FOUND in playlist [{sp_playlist}] with owner [{sp_playlist_owner}] and uri [{sp_playlist_uri}]")
                            #sp_playlist = sp_playlist + ICON_SONG_MISSING_FROM_PLAYLIST
                            if ALT_VIEW and JMK_MODE: # 'hasTrack' is a JMK-specific code change
                                icon_add = True
                            # sp_playlist = "unknown - error"
                            # is_playlist = False
            else:
                hasTrack = False
                sp_playlist_image_url = ""

# this section is executed only during first boot up of script
# ------------------------------------------------------------
            print_debug(f"LOOP A - FIRST BOOT UP")
            # must be in front of possible 'icon' appending or search URLs will errantly include the icon
            context_m_body = ""
            context_m_body_html = ""
            apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))
            # apple_search_url, genius_search_url, youtube_music_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))

            dz_str = f"{sp_artist} - {sp_track}"

            last_found_playlist = found_playlist
            if not hasTrack and (sp_playlist_owner != "Spotify"):
                found_playlist = find_song_in_playlists(dz_str, found_playlist, sp_playlist if is_playlist else "")
            else:
                found_playlist = False
                last_found_playlist = False
                print_debug(f"SKIPPED FIND_SONG IN_PLAYLIST (1A) -> hasTrack: {hasTrack}")                   

            # if song is not in currently tracked playlist, but a different one, it might be an exception or the start of a new detected playlist
            if found_playlist and last_found_playlist and (found_playlist.get('name', 'A') != last_found_playlist.get('name', 'B')):
            # if this song puts currently tracked playlist over the exception limit, then it can be start of a newly detected playlist
#jmkfix can this case every happen. is it in log?
                if last_found_playlist['count_end'] >= (last_found_playlist['qty_end']):
                    new_playlist = True
                    print_debug(f"SPECIAL CASE: SONG IN ANOTHER MONITORED PLAYLIST, AT EXCEPTION LIMIT FOR CURRENT (1) - old: {last_found_playlist.get('name', 'A')} new: {found_playlist.get('name', 'A')}")
                    reset_playlist_counts() 
                    ridden = False
            # else it should be considered an exception
#jmkfix can this case every happen. is it in log?
                else:
                    print_debug(f"SPECIAL CASE: SONG EXCEPTION BUT IN ANOTHER MONITORED PLAYLIST (1)")
                    new_playlist = False
            else:
                new_playlist = True

            # playlist detected
            # if playlist changed, need to handle it as an exception first
            if found_playlist and new_playlist:
                print_debug(f"FOUND PLAYLIST IN MONITORING LIST (1) -> {found_playlist['name']}")
                print_debug(f"COUNT START: {found_playlist['count_start']}, {found_playlist['qty_start']}")
                reset_playlist_counts(found_playlist['name'] if found_playlist else "")
                found_playlist['count_start'] += 1
                print_debug(f"COUNT START +1: {found_playlist['count_start']}")
                if found_playlist.get('override', OVERRIDE_PLAYLIST_AT_START):
                    print_debug(f"FIRST BOOT PLAYLIST COUNT OVERRIDE")
                    print_debug(f"OVERRIDE COUNT (1): from {found_playlist['count_start']} to {found_playlist['qty_start']}")
                    if found_playlist['count_start'] < found_playlist['qty_start']:
                        found_playlist['count_start'] = found_playlist['qty_start']
                        count_overridden = True
                if found_playlist['count_start'] >= found_playlist['qty_start']:
                    print_debug(f"PLAYLIST_DETECTED (1): {found_playlist['count_start']}, {found_playlist['qty_start']}")
                    is_playlist = True
                    sp_playlist = found_playlist['name']
                    sp_playlist_url = found_playlist.get('url', '')
                    sp_track = sp_track + found_playlist.get('icon', '')
                    playlist_m_body = f"\nPlaylist: {sp_playlist}{iconstring()}"
                    playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}{iconstring()}</a>"

                dz_message = build_dz_string(found_playlist)
                if DEBUG_JMK and dz_message != "":
                    dz_message = dz_message + " (2)"
                body_dz = dz_message + "\n"
                body_dz_html = dz_message + "<br>"

            else:
                if DEBUG_JMK and not found_playlist:
                    print_debug(f"SONG NOT IN A MONITORED PLAYLIST (1)")
                # reset_playlist_counts()

                # process a possible exception if last song was in a playlist (even if as exception) AND it's an active playlist (not counting up towards it)
                # actually, if not allowing exception during counting up to > 2, may never get there since smart shuffle puts a new song every 3
                # if last_found_playlist and (last_found_playlist['count_start'] >= last_found_playlist['qty_start']):
                if last_found_playlist:
                    print_debug(f"COUNT END: {last_found_playlist['count_end']}")
                    last_found_playlist['count_end'] += 1
                    print_debug(f"COUNT END + 1: {last_found_playlist['count_end']}")
                    if found_playlist:
                        found_playlist['count_start'] += 1
                        print_debug(f"COUNT START + 1 - {found_playlist['name']}: {found_playlist['count_start']}")
                    if last_found_playlist['count_end'] >= last_found_playlist['qty_end']:
                        reset_playlist_counts(found_playlist['name'] if found_playlist else "")
                        count_overridden = False
                        # body_dz = ""
                        # body_dz_html = ""
                        # dz_message = ""
                    else:
                        # since haven't hit limit yet to consider playlist over, set found_playlist back to previous
                        found_playlist = last_found_playlist
                        is_playlist = True
                        sp_playlist = found_playlist['name']
                        sp_playlist_url = found_playlist.get('url', '')
                        playlist_m_body = f"\nPlaylist: {sp_playlist}{iconstring()}"
                        playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}</a>"
                        print_debug(f"COUNT_SHUFFLE: {found_playlist['count_shuffle']}")
                        found_playlist['count_shuffle'] += 1
                        print_debug(f"COUNT SHUFFLE + 1: {found_playlist['count_shuffle']}")
                        # don't show icon in this case, but OK to show playlist with an *
                        # sp_track = sp_track + found_playlist.get('icon', '')
                        if ALT_VIEW:
                            icon_add = True
                        print_debug(f"HAVEN'T HIT LIMIT TO DISCONTINUE PLAYLIST (1) -> {found_playlist['name']}")
                else:
                    reset_playlist_counts()
                    count_overridden = False
                    # body_dz = ""
                    # body_dz_html = ""
                    # dz_message = ""

            print(f"Username:\t\t\t{sp_username}")
            print(f"User URI ID:\t\t\t{sp_data['sp_uri']}")
            print(f"\nLast played:\t\t\t{sp_artist} - {sp_track}")
            print(f"Duration:\t\t\t{display_time(sp_track_duration)}\n")
            if is_playlist:
                print(f"Playlist:\t\t\t{sp_playlist}{playlist_suffix}")

            print(f"Album:\t\t\t\t{sp_album}")

            if JMK_MODE:
                if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
                    print(f"\nContext (Album):\t\t{sp_playlist}")
                    context_m_body += f"\nContext (Album): {sp_playlist}"
                    context_m_body_html += f"<br>Context (Album): <a href=\"{spotify_convert_uri_to_url(sp_playlist_uri)}\">{escape(sp_playlist)}</a>"
            else:
                if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
                    print(f"\nContext (Album):\t\t{sp_playlist}")
                    context_m_body += f"\nContext (Album): {sp_playlist}"
                    context_m_body_html += f"<br>Context (Album): <a href=\"{spotify_convert_uri_to_url(sp_playlist_uri)}\">{escape(sp_playlist)}</a>"

            if 'spotify:artist:' in sp_playlist_uri:
                print(f"\nContext (Artist):\t\t{sp_playlist}")
                context_m_body += f"\nContext (Artist): {sp_playlist}"
                context_m_body_html += f"<br>Context (Artist): <a href=\"{spotify_convert_uri_to_url(sp_playlist_uri)}\">{escape(sp_playlist)}</a>"

            print(f"\nTrack URL:\t\t\t{sp_track_url}")
            if is_playlist:
                print(f"Playlist URL:\t\t\t{sp_playlist_url}")
            print(f"Album URL:\t\t\t{sp_album_url}")

#jmk        if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
            if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
                print(f"Context (Album) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

            if 'spotify:artist:' in sp_playlist_uri:
                print(f"Context (Artist) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

            apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))

            music_urls_output = format_music_urls_console(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
            if music_urls_output:
                print(music_urls_output)
            lyrics_output = format_lyrics_urls_console(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
            if lyrics_output:
                print(lyrics_output)

            if not is_playlist:
                sp_playlist = ""

            print(f"\nLast activity:\t\t\t{get_date_from_ts(sp_ts)} ({calculate_timespan(int(time.time()), sp_ts)} ago)")

            # Friend is currently active (listens to music)
            if (cur_ts - sp_ts) <= SPOTIFY_INACTIVITY_CHECK:
                active_ever = True # added 2/28/2026
                print_debug(f"ACTIVE EVER: {active_ever} (0)")
                print_debug(f"LOOP A - BOOT - FRIEND ACTIVE")
                if JMK_MODE:
                    sp_active_ts_start = sp_ts # reset start time to [00] instead starting at length of the first song (ex:[04])
                else:
                    sp_active_ts_start = sp_ts - sp_track_duration
                sp_active_ts_stop = 0
                listened_songs = 1
                song_on_loop = 1
                recent_songs_session = [{'artist': sp_artist, 'track': sp_track, 'timestamp': sp_ts, 'skipped': False}]
                print_debug(f"ACTIVE EVER: {active_ever} (1)")
                print("\n*** Friend is currently ACTIVE !")

                if FLAG_FILE:
                    flag_file_create()

                if sp_track.upper() in tracks_upper or sp_playlist.upper() in tracks_upper or sp_album.upper() in tracks_upper:
                    print("*** Track/playlist/album matched with the list!")

                try:
                    if csv_file_name:
                        write_csv_entry(csv_file_name, datetime.fromtimestamp(int(cur_ts)), sp_artist, sp_track, sp_playlist, sp_album, datetime.fromtimestamp(int(sp_ts)))
                except Exception as e:
                    print(f"* Error: {e}")
                jmk_send = True

                if ACTIVE_NOTIFICATION:
                    music_urls_text = format_music_urls_email_text(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                    music_urls_html = format_music_urls_email_html(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url, sp_artist, sp_track)
                    lyrics_urls_text = format_lyrics_urls_email_text(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                    lyrics_urls_html = format_lyrics_urls_email_html(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, sp_artist, sp_track)
                    if music_urls_text:
                        music_section_text = f"\n\n{music_urls_text}"
                        music_section_html = f"<br><br>{music_urls_html}"
                        lyrics_section_text = f"\n{lyrics_urls_text}\n\n" if lyrics_urls_text else "\n\n"
                        lyrics_section_html = f"<br>{lyrics_urls_html}<br><br>" if lyrics_urls_html else "<br><br>"
                    else:
                        if lyrics_urls_text:
                            music_section_text = "\n\n"
                            music_section_html = "<br><br>"
                            lyrics_section_text = f"{lyrics_urls_text}\n\n"
                            lyrics_section_html = f"{lyrics_urls_html}<br><br>"
                        else:
                            music_section_text = "\n\n"
                            music_section_html = "<br><br>"
                            lyrics_section_text = ""
                            lyrics_section_html = ""
                    m_subject = f"Spotify user {sp_username} is active: '{sp_artist} - {sp_track}'"
                    m_body = f"Last played: {sp_artist} - {sp_track}\nDuration: {display_time(sp_track_duration)}{playlist_m_body}\nAlbum: {sp_album}{context_m_body}{music_section_text}{lyrics_section_text}Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})\n\nLast activity: {get_date_from_ts(sp_ts)}{get_cur_ts(nl_ch + 'Timestamp: ')}"
                    m_body_html = f"<html><head></head><body>Last played: <b><a href=\"{sp_artist_url}\">{escape(sp_artist)}</a> - <a href=\"{sp_track_url}\">{escape(sp_track)}</a></b><br>Duration: {display_time(sp_track_duration)}{playlist_m_body_html}<br>Album: <a href=\"{sp_album_url}\">{escape(sp_album)}</a>{context_m_body_html}{music_section_html}{lyrics_section_html}Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})<br><br>Last activity: {get_date_from_ts(sp_ts)}{get_cur_ts('<br>Timestamp: ')}</body></html>"
                    print(f"Sending email notification to {RECEIVER_EMAIL}")
                    if JMK_MODE:
                        update_spreadsheet_row(SPREADSHEET_DIVIDER_TEXT, False)
                        send_email(f"{GMAIL_TAG}---------------------------------", "  ", "  ", SMTP_SSL)
                        song_footer_txt, song_footer_html = update_spreadsheet_row(f"{datetime.now().strftime('%H:%M:%S')} {songstring()}", True)
                        m_body += song_footer_txt
                        m_body_html = m_body_html.replace("</body></html>", song_footer_html + "</body></html>")
                        send_email(f"{GMAIL_TAG}[{time_diff_str()}] {timestring()} {songstring()}", m_body, m_body_html, SMTP_SSL)
                    if not JMK_MODE or ORIG_EMAILS:
                        send_email(m_subject, m_body, m_body_html, SMTP_SSL)

                if TRACK_SONGS and sp_track_uri_id:
                    if platform.system() == 'Darwin':       # macOS
                        spotify_macos_play_song(sp_track_uri_id)
                    elif platform.system() == 'Windows':    # Windows
                        spotify_win_play_song(sp_track_uri_id)
                    else:                                   # Linux variants
                        spotify_linux_play_song(sp_track_uri_id)

            # Friend is currently offline (does not play music)
            else:
                print_debug(f"LOOP A - BOOT - FRIEND INACTIVE")
                sp_active_ts_stop = sp_ts
                print(f"\n*** Friend is OFFLINE for: {calculate_timespan(int(cur_ts), int(sp_ts))}")

            if listened_songs:
                print(f"\nSongs played:\t\t\t{listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})")

            print(f"")
            for playlist_name, playlist_data in monitored_playlists_data.items():
#                print(f"Monitoring Tracks: {playlist_name} ({len(playlist_data.get('tracks_set'))} songs)")
#                print(f"Monitoring Tracks [alerts: {f'{str(playlist_data.get('notify')).lower()},':<6} refresh: {playlist_data.get('refresh'):>4}]: {playlist_name} ({len(playlist_data.get('tracks_set'))} songs)")
                # these must be broken out to avoid quoting issues with the justifications
                alerts_status_str = f"{str(playlist_data.get('notify', NOTIFY_PLAYLIST_DETECTED)).lower()},"
                refresh_value = playlist_data.get('refresh', LOAD_TRACKS_FREQUENCY)
                print(f"Monitoring Tracks [alerts: {alerts_status_str:<6} refresh: {refresh_value:>4}]: {playlist_name} ({len(playlist_data.get('tracks_set'))} songs)")
            if dz_message or listened_songs:
                print("")
            if dz_message:
                print(dz_message)

            print_cur_ts("\nTimestamp:\t\t\t")

            sp_ts_old = sp_ts
            alive_counter = 0

            email_sent = False

            # Change print's beyond this point to only go to log
            # Then, print_to_screen will only go to screen (both a possibility for debugging)
            if ALT_VIEW:
                sys.stdout = Logger(FINAL_LOG_PATH, mode="log")

            # Print after timestamp
            if ALT_VIEW and jmk_send:
                print_debug(f"JMK SEND")
#                song_count = 1
                print_to_screen(f" ")
                print_to_screen(f"----------------------")               
#                print_to_both(f"{timestring()}: {ERR_CODE}, *** Start text sent. Track: {songstring()}")
                print_to_both(f"{timestring()}: {ERR_CODE}, *** Start notification sent")
                #---
#                dz_str = f"{sp_artist} - {sp_track}"
                if not hasTrack and (sp_playlist_owner != "Spotify"):
                    found_playlist = find_song_in_playlists(dz_str, found_playlist, sp_playlist if is_playlist else "")
                else:
                    found_playlist = False
                    print_debug(f"SKIPPED FIND_SONG_IN_PLAYLIST (1B) -> hasTrack: {hasTrack}")                   
                print_debug(f"PLAYLIST CHECK: {found_playlist}, {dz_str}")
# this is executed during first boot up only
                if found_playlist:
                    print_debug(f"PLAYLIST FOUND: count: {found_playlist['count_start']}")
                    if found_playlist['count_start'] >= found_playlist['qty_start']:
                        print_debug(f"BOOTUP PLAYLIST DETECTED")
                        print_debug(f"PLAYLIST_DETECT (1): {found_playlist['count_start']}")
                        body_dz, body_dz_html, dz_message, dz_msg_screen = monitored_playlist_detected(found_playlist, songstring(), time_diff_str(), True, sp_track, sp_artist, sp_album)
                    else:
                        dz_message = build_dz_string(found_playlist)
                        if DEBUG_JMK and dz_message != "":
                            dz_message = dz_message + " (3)"

                print_to_screen(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}")
                send_notification(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}", sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '', time_diff_str(), listened_songs)

                if SEND_NOTIFY:
                    # send_notification(f"START: {songstring()}", sp_album_image_url)
                    send_notification(f"START: {songstring()}", sp_playlist_image_url if sp_playlist_image_url else sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '')

                    # if dz_message:
                        # send_notification(dz_message)
            disappeared_counter = 0

            playlist_suffix = ""
            if ALT_VIEW:
                icon_add = False
            hastrack = False
            print_debug(f"LOOP B - PRIMARY LOOP")
            # Primary loop
            while True:

                while True:
                    # Sometimes Spotify network functions halt even though we specified the timeout
                    # To overcome this we use alarm signal functionality to kill it inevitably, not available on Windows
                    if platform.system() != 'Windows':
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(ALARM_TIMEOUT)
                    try:
                        if TOKEN_SOURCE == "client":
                            sp_accessToken = spotify_get_access_token_from_client_auto(DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN)
                        else:
                            sp_accessToken = spotify_get_access_token_from_sp_dc(SP_DC_COOKIE)

                        sp_accessToken_oauth_app = spotify_get_access_token_from_oauth_app(SP_APP_CLIENT_ID, SP_APP_CLIENT_SECRET)

                        sp_friends = spotify_get_friends_json(sp_accessToken)
                        sp_found, sp_data = spotify_get_friend_info(sp_friends, user_uri_id)
                        email_sent = False
                        if platform.system() != 'Windows':
                            signal.alarm(0)
                        break
                    except TimeoutException:
                        if platform.system() != 'Windows':
                            signal.alarm(0)
                        print(f"spotify_*() function timeout after {display_time(ALARM_TIMEOUT)}, retrying in {display_time(ALARM_RETRY)}")
                        print_cur_ts("Timestamp:\t\t\t")
                        time.sleep(ALARM_RETRY)
                    except Exception as e:
                        if platform.system() != 'Windows':
                            signal.alarm(0)

                        err = str(e).lower()

                        if TOKEN_SOURCE == 'cookie' and '401' in err:
                            SP_CACHED_ACCESS_TOKEN = None

                        str_matches = ["500 server", "504 server", "502 server", "503 server"]
                        if any(x in err for x in str_matches):
                            if not error_500_start_ts:
                                error_500_start_ts = int(time.time())
                                error_500_counter = 1
                            else:
                                error_500_counter += 1

                        str_matches = ["timed out", "timeout", "name resolution", "failed to resolve", "family not supported", "429 client", "aborted"]
                        if any(x in err for x in str_matches) or str(e) == '':
                            if not error_network_issue_start_ts:
                                error_network_issue_start_ts = int(time.time())
                                error_network_issue_counter = 1
                            else:
                                error_network_issue_counter += 1

                        if error_500_start_ts and (error_500_counter >= ERROR_500_NUMBER_LIMIT and (int(time.time()) - error_500_start_ts) >= ERROR_500_TIME_LIMIT):
                            print(f"* Error 50x ({error_500_counter}x times in the last {display_time((int(time.time()) - error_500_start_ts))}): '{e}'")
                            print_cur_ts("Timestamp:\t\t\t")
                            error_500_start_ts = 0
                            error_500_counter = 0

                        elif error_network_issue_start_ts and (error_network_issue_counter >= ERROR_NETWORK_ISSUES_NUMBER_LIMIT and (int(time.time()) - error_network_issue_start_ts) >= ERROR_NETWORK_ISSUES_TIME_LIMIT):
                            print(f"* Error with network ({error_network_issue_counter}x times in the last {display_time((int(time.time()) - error_network_issue_start_ts))}): '{e}'")
                            print_cur_ts("Timestamp:\t\t\t")
                            error_network_issue_start_ts = 0
                            error_network_issue_counter = 0

                        elif not error_500_start_ts and not error_network_issue_start_ts:
                            print(f"* Error, retrying in {display_time(SPOTIFY_ERROR_INTERVAL)}: '{e}'")

                            client_errs = ['access token', 'invalid client token', 'expired client token', 'refresh token has been revoked', 'refresh token has expired', 'refresh token is invalid', 'invalid grant during refresh']
                            cookie_errs = ['access token', 'unauthorized', 'unsuccessful token request']

                            if TOKEN_SOURCE == 'client' and any(k in err for k in client_errs):
                                print(f"* Error: client or refresh token may be invalid or expired!")
                                if ERROR_NOTIFICATION and not email_sent:
                                    m_subject = f"spotify_monitor: client or refresh token may be invalid or expired! (uri: {user_uri_id})"
                                    m_body = f"Client or refresh token may be invalid or expired!\n{e}{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                                    m_body_html = f"<html><head></head><body>Client or refresh token may be invalid or expired!<br>{escape(str(e))}{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                                    print(f"Sending email notification to {RECEIVER_EMAIL}")
                                    send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                                    email_sent = True

                            elif TOKEN_SOURCE == 'cookie' and any(k in err for k in cookie_errs):
                                print(f"* Error: sp_dc may be invalid/expired or Spotify has broken sth again!")
                                if ERROR_NOTIFICATION and not email_sent:
                                    m_subject = f"spotify_monitor: sp_dc may be invalid/expired or Spotify has broken sth again! (uri: {user_uri_id})"
                                    m_body = f"sp_dc may be invalid/expired or Spotify has broken sth again!\n{e}{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                                    m_body_html = f"<html><head></head><body>sp_dc may be invalid/expired or Spotify has broken sth again!<br>{escape(str(e))}{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                                    print(f"Sending email notification to {RECEIVER_EMAIL}")
                                    send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                                    email_sent = True

                            print_cur_ts("Timestamp:\t\t\t")
                        time.sleep(SPOTIFY_ERROR_INTERVAL)

                if sp_found is False:
                    # User has disappeared from the Spotify's friend list or account has been removed
                    disappeared_counter += 1
                    if disappeared_counter < REMOVED_DISAPPEARED_COUNTER:
                        time.sleep(SPOTIFY_CHECK_INTERVAL)
                        continue
                    if user_not_found is False:
                        if is_user_removed(sp_accessToken_oauth_app, user_uri_id, oauth_app=True):
                            print(f"Spotify user '{user_uri_id}' ({sp_username}) was probably removed! Retrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals")
                            if ERROR_NOTIFICATION:
                                m_subject = f"Spotify user {user_uri_id} ({sp_username}) was probably removed!"
                                m_body = f"Spotify user {user_uri_id} ({sp_username}) was probably removed\nRetrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                                m_body_html = f"<html><head></head><body>Spotify user {user_uri_id} (<b>{sp_username}</b>) was probably removed<br>Retrying in <b>{display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)}</b> intervals{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                                print(f"Sending email notification to {RECEIVER_EMAIL}")
                                send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                        else:
                            print(f"Spotify user '{user_uri_id}' ({sp_username}) has disappeared - make sure your friend is followed and has activity sharing enabled. Retrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals")
                            if ERROR_NOTIFICATION:
                                m_subject = f"Spotify user {user_uri_id} ({sp_username}) has disappeared!"
                                m_body = f"Spotify user {user_uri_id} ({sp_username}) has disappeared - make sure your friend is followed and has activity sharing enabled\nRetrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                                m_body_html = f"<html><head></head><body>Spotify user {user_uri_id} (<b>{sp_username}</b>) has disappeared - make sure your friend is followed and has activity sharing enabled<br>Retrying in <b>{display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)}</b> intervals{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                                print(f"Sending email notification to {RECEIVER_EMAIL}")
                                send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                        print_cur_ts("Timestamp:\t\t\t")
                        user_not_found = True
                    time.sleep(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)
                    continue
                else:
                    # User reappeared in the Spotify's friend list
                    disappeared_counter = 0
                    if user_not_found is True:
                        print(f"Spotify user {user_uri_id} ({sp_username}) has reappeared!")
                        if ERROR_NOTIFICATION:
                            m_subject = f"Spotify user {user_uri_id} ({sp_username}) has reappeared!"
                            m_body = f"Spotify user {user_uri_id} ({sp_username}) has reappeared!{get_cur_ts(nl_ch + nl_ch + 'Timestamp: ')}"
                            m_body_html = f"<html><head></head><body>Spotify user {user_uri_id} (<b>{sp_username}</b>) has reappeared!{get_cur_ts('<br><br>Timestamp: ')}</body></html>"
                            print(f"Sending email notification to {RECEIVER_EMAIL}")
                            send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                        print_cur_ts("Timestamp:\t\t\t")

                user_not_found = False
                sp_ts = sp_data["sp_ts"]
                cur_ts = int(time.time())
                # Track has changed
                if sp_ts != sp_ts_old:
                    sp_artist_old = sp_artist
                    sp_track_old = sp_track
                    alive_counter = 0
#                    song_count += 1
                    sp_playlist = sp_data["sp_playlist"]
                    if JMK_MODE:
                        if sp_playlist == "Discovery zone":
                            sp_playlist = "Discovery Zone"
                    sp_track_uri = sp_data["sp_track_uri"]
                    sp_track_uri_id = sp_data["sp_track_uri_id"]
                    sp_album_uri = sp_data["sp_album_uri"]
                    sp_playlist_uri = sp_data["sp_playlist_uri"]
                    try:
                        sp_track_data = spotify_get_track_info(sp_accessToken_oauth_app, sp_track_uri, oauth_app=True)
                        is_playlist = 'spotify:playlist:' in sp_playlist_uri
                        if is_playlist:
                            sp_playlist_owner = spotify_get_playlist_owner(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                            sp_playlist_image_url = spotify_get_playlist_image_url(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                            playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""
                            playlist_suffix += (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")
                    except Exception as e:
                        print(f"* Error, retrying in {display_time(SPOTIFY_ERROR_INTERVAL)}: {e}")
                        print_cur_ts("Timestamp:\t\t\t")
                        time.sleep(SPOTIFY_ERROR_INTERVAL)
                        continue

                    sp_username = sp_data["sp_username"]

                    sp_artist = sp_data["sp_artist"]
                    if not sp_artist:
                        sp_artist = sp_track_data["sp_artist_name"]

                    sp_track = sp_data["sp_track"]
                    if not sp_track:
                        sp_track = sp_track_data["sp_track_name"]

                    sp_album = sp_data["sp_album"]
                    if not sp_album:
                        sp_album = sp_track_data["sp_album_name"]

                    sp_album_image_url = sp_track_data["sp_album_image_url"]
                    if not sp_album_image_url:
                        sp_album_image_url = ""

                    sp_track_duration = sp_track_data["sp_track_duration"]
                    sp_track_url = sp_track_data["sp_track_url"]
                    sp_artist_url = sp_track_data["sp_artist_url"]
                    sp_album_url = sp_track_data["sp_album_url"]

                    # If tracking functionality is enabled then play the current song via Spotify client

                    if TRACK_SONGS and sp_track_uri_id:
                        if platform.system() == 'Darwin':       # macOS
                            spotify_macos_play_song(sp_track_uri_id)
                        elif platform.system() == 'Windows':    # Windows
                            spotify_win_play_song(sp_track_uri_id)
                        else:                                   # Linux variants
                            spotify_linux_play_song(sp_track_uri_id)

                    if is_playlist:
                        # sp_playlist_owner = sp_playlist_data.get("sp_playlist_owner")
                        sp_playlist_owner = spotify_get_playlist_owner(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                        playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""
                        playlist_suffix += (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")

                        if JMK_MODE:
                            hasTrack = (sp_playlist_owner == "Spotify") or (search_playlist(sp_accessToken_oauth_app, sp_playlist, sp_playlist_uri, sp_track_uri_id, sp_track, sp_artist, False))
                            print_debug(f"hasTrack (B1): {hasTrack}, sp_playlist_owner: {sp_playlist_owner}, sp_playlist: {sp_playlist}")
                            if hasTrack:
                                for playlist_data in monitored_playlists_data.values():
                                    if sp_playlist and (sp_playlist.upper() == playlist_data.get('name', "B").upper()):
                                        hasTrack = False
                                        print_debug(f"hastrack Playlist Match (B2a): hastrack = FALSE, sp_playlist: {sp_playlist}")
                                print_debug(f"hasTrack (B2b): {hasTrack}, sp_playlist: {sp_playlist}")

                            print_debug(f"hasTrack (B3): {hasTrack}, sp_playlist_owner: {sp_playlist_owner}")

                            if not hasTrack:
                                if (sp_playlist_owner != "Spotify"):
                                    print_debug(f"SONG NOT IN REPORTED PLAYLIST (2)")
                                    print_to_log(f"ERROR: track: {sp_track}, NOT FOUND in playlist: {sp_playlist} ({sp_track})")
    #                                sp_playlist = sp_playlist + ICON_SONG_MISSING_FROM_PLAYLIST
                                    if ALT_VIEW and JMK_MODE: # 'hasTrack' is a JMK-specific code change
                                        icon_add = True
                                    # sp_playlist = "unknown - error"
                                    # is_playlist = False
                    else:
                        hasTrack = False

                    if is_playlist:
                        sp_playlist_url = spotify_convert_uri_to_url(sp_playlist_uri)
                        sp_playlist_image_url = spotify_get_playlist_image_url(sp_accessToken_oauth_app, sp_playlist_uri, oauth_app=True)
                        # sp_playlist_image_url = sp_playlist_data.get("sp_playlist_image_url", "")
                        playlist_m_body = f"\nPlaylist: {sp_playlist}{playlist_suffix}"
                        playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}{playlist_suffix}</a>"
                    else:
                        playlist_m_body = ""
                        playlist_m_body_html = ""
                        sp_playlist_image_url = ""

                    if sp_artist == sp_artist_old and sp_track == sp_track_old:
                        song_on_loop += 1
                        if song_on_loop == SONG_ON_LOOP_VALUE:
                            looped_songs += 1
                    else:
                        song_on_loop = 1

                    if sp_active_ts_start == 0:
                        sp_active_ts_start = sp_ts     
# this is executed for every song change
# is that true?
# below definitely does ("SONG NOT IN A MONITORED PLAYLIST (2)")
# what's the difference?
                    print_debug(f"LOOP C - FOR ALL SONGS")
                    # move this in front of possible 'icon' appending or that will impact search URLs
                    # apple_search_url, genius_search_url, youtube_music_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))
                    apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))

                    print_debug(f"SONG CHANGE -> {sp_artist} - {sp_track}")
                    print_debug(f"ACTIVE EVER: {active_ever} (2)")
                    print_debug(f"hasTrack: {hasTrack}")
                    #---
                    dz_msg_screen = ""
                    dz_str = f"{sp_artist} - {sp_track}"
                    last_found_playlist = found_playlist
                    if not hasTrack:
                        found_playlist = find_song_in_playlists(dz_str, found_playlist, sp_playlist if is_playlist else "")
                    else:
                        # DZ cleared is lost here - 2/28/2026 try to fix #jmk
                        if active_ever and last_found_playlist:
                            print_debug(f"last_found_playlist: {last_found_playlist}")
                            print_debug(f"songstring(): {songstring}, time_diff_str: {time_diff_str}")
                            print_debug(f"sp_track: {sp_track}, sp_artist: {sp_artist}, sp_album: {sp_album}")
                            dz_message, dz_msg_screen = monitored_playlist_cleared(last_found_playlist, songstring(), time_diff_str(), sp_track, sp_artist, sp_album)
                            print_debug(f"dz_message: {dz_message}, dz_msg_screen: {dz_msg_screen}")
                            if ALT_VIEW:
                                print_to_screen(dz_msg_screen) # could get overwritten in next section
                                dz_msg_screen = "" # prevent duplicate printing below
                        # reset after 'monitored_playlist_cleared' to ensure 'song count' is available for it
                        reset_playlist_counts(found_playlist['name'] if found_playlist else "") 
                        count_overridden = False
                        # DZ cleared is lost here - 2/28/2026 try to fix #jmk

                        # copied above here from just below where it's not triggering due to the next two lines
                        found_playlist = False
                        last_found_playlist = False
                        
                        print_debug(f"SKIPPED FIND_SONG_IN_PLAYLIST (2) -> hasTrack: {hasTrack}")                   
                    # if song is not in currently tracked playlist, but a different one, it might be an exception or the start of a new detected playlist
                    if DEBUG_JMK:
                        if found_playlist:
                            print_debug(f"playlist A: {found_playlist.get('name', 'A')}")
                        if last_found_playlist:
                            print_debug(f"playlist B: {last_found_playlist.get('name', 'B')}")
                    if found_playlist and last_found_playlist and (found_playlist.get('name', 'A') != last_found_playlist.get('name', 'B')):
                    # if this song puts currently tracked playlist over the exception limit, then it can be start of a newly detected playlist
                        print_debug(f"count_end: {last_found_playlist['count_end']}, qty_end: {last_found_playlist['qty_end']}")
                        if last_found_playlist['count_end'] >= (last_found_playlist['qty_end']):
                            new_playlist = True
                            print_debug(f"SPECIAL CASE: SONG IN ANOTHER MONITORED PLAYLIST, AT EXCEPTION LIMIT FOR CURRENT (2) - old: {last_found_playlist.get('name', 'A')} new: {found_playlist.get('name', 'A')}")
                            # force notify_playlist_cleared before going down code path for new playlist
                            # skip if never active after boot, because any existing monitored playlist was 'assumed'
                            print_debug(f"ACTIVE EVER: {active_ever} (2)")
                            if active_ever:
                                dz_message, dz_msg_screen = monitored_playlist_cleared(last_found_playlist, songstring(), time_diff_str(), sp_track, sp_artist, sp_album)
                            if ALT_VIEW:
                                print_to_screen(dz_msg_screen) # could get overwritten in next section
                                dz_msg_screen = "" # prevent duplicate printing below
                            # reset after 'monitored_playlist_cleared' to ensure 'song count' is available for it
                            reset_playlist_counts(found_playlist['name'] if found_playlist else "") 
                            count_overridden = False
                    # else it should be considered an exception
                        else:
                            print_debug(f"SPECIAL CASE: SONG EXCEPTION BUT IN ANOTHER MONITORED PLAYLIST (2): count_end: {last_found_playlist['count_end']} qty_end: {last_found_playlist['qty_end']}")
                            new_playlist = False
                    else:
                        new_playlist = True

                    # playlist detected
                    # if playlist changed, need to handle it as an exception first
                    if found_playlist and new_playlist:
                        print_debug(f"FOUND PLAYLIST IN MONITORING LIST (2) -> {found_playlist['name']}")
                        print_debug(f"COUNT START: {found_playlist['count_start']}, {found_playlist['qty_start']}")
                        reset_playlist_counts(found_playlist['name'] if found_playlist else "")
                        found_playlist['count_start'] += 1
                        print_debug(f"COUNT START + 1: {found_playlist['count_start']}")

                        # count was high enough to trigger detection
                        if found_playlist['count_start'] >= found_playlist['qty_start']:
                            print_debug(f"PLAYLIST_DETECTED (2): {found_playlist['count_start']}, {found_playlist['qty_start']}")
                            is_playlist = True
                            sp_playlist = found_playlist['name']
                            sp_playlist_url = found_playlist.get('url', '')
                            sp_track = sp_track + found_playlist.get('icon', '')
                            playlist_m_body = f"\nPlaylist: {sp_playlist}{iconstring()}"
                            playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}</a>"
    
                        # active user check
                        if not ((cur_ts - sp_ts_old) > SPOTIFY_INACTIVITY_CHECK and sp_active_ts_stop > 0):
                            # enough to start playlist?
                            if found_playlist['count_start'] == found_playlist['qty_start']:
                                print_debug(f"PLAYLIST_DETECT (2): {found_playlist['count_start']}")
                                body_dz, body_dz_html, dz_message, dz_msg_screen = monitored_playlist_detected(found_playlist, songstring(), time_diff_str(), False, sp_track, sp_artist, sp_album) # False is because dz_msg_screen is printed below in sequence after the song name gets printed
                            else:
                            # not enough to start playlist
                                dz_message = build_dz_string(found_playlist)
                                if DEBUG_JMK and dz_message != "":
                                    dz_message = dz_message + " (4a)"
                                    print_debug(f"DZ_MESSAGE (4a) -> {dz_message}")
                        else:
                        # inactive user (but going active?)
                            dz_message = build_dz_string(found_playlist)
                            if DEBUG_JMK and dz_message != "":
                                dz_message = dz_message + " (4b)"
                                print_debug(f"DZ_MESSAGE (4b) -> {dz_message}")

                        body_dz = dz_message + "\n"
                        body_dz_html = dz_message + "<br>"

                    # playlist NOT detected or an exception
                    else:
# handled in section further below if someone just became active
# this check handles if NOT just becoming active
                        if DEBUG_JMK and not found_playlist:
                            print_debug(f"SONG NOT IN A MONITORED PLAYLIST (2)")
                        else:
                            print_debug(f"SONG FOUND IN A MONITORED PLAYLIST (2)")                       
                        # check for user just becoming active - if so, proceed
                        #7/31/25 do we need this next line? (found_checklist doesn't have it)
                        # if ((cur_ts - sp_ts_old) > SPOTIFY_INACTIVITY_CHECK and sp_active_ts_stop > 0):
                        # (all below was intented to above line)
                        # this is case where playlist not found BUT it was previously found (so either lost or count exceptions)
                        # dz_message = ""
                        # dz_message_screen = ""
                        # body_dz = ""
                        # body_dz_html = ""
                        # reset_playlist_counts()

                        # process a possible exception if last song was in a playlist (even if as exception) AND it's an active playlist (not counting up towards it)
                        # actually, if not allowing exception during counting up to > 2, may never get there since smart shuffle puts a new song every 3
                        # if last_found_playlist and (last_found_playlist['count_start'] >= last_found_playlist['qty_start']):
                        print_debug(f"ACTIVE USER, CHECKING FOR PLAYLIST (2)")
                        if last_found_playlist:
                            print_debug(f"BUT LAST SONG WAS IN PLAYLIST")
                            print_debug(f"COUNT END - {last_found_playlist['name']}: {last_found_playlist['count_end']}")
                            last_found_playlist['count_end'] += 1
                            print_debug(f"COUNT END + 1 - {last_found_playlist['name']}: {last_found_playlist['count_end']}")
                            if found_playlist:
                                found_playlist['count_start'] += 1
                                print_debug(f"COUNT START + 1 - {found_playlist['name']}: {found_playlist['count_start']}")

                            print_debug(f"count_end: {last_found_playlist['count_end']}, qty_end: {last_found_playlist['qty_end']}")

                            if last_found_playlist['count_end'] >= last_found_playlist['qty_end']:
                                # limit achieved
                                # 7/31: actually don't want to show a "cleared" message when first coming up
                                # dz_message, dz_msg_screen = monitored_playlist_cleared(last_found_playlist, songstring(), time_diff_str())
                                #jmkfix 08/04 this DEFINITELY also runs during runtime
                                # only clear if last playlist was active
                                if last_found_playlist['count_start'] >= last_found_playlist['qty_start']:
                                    dz_message, dz_msg_screen = monitored_playlist_cleared(last_found_playlist, songstring(), time_diff_str(), sp_track, sp_artist, sp_album)

                                #jmkfix 2/28/2026
                                if ALT_VIEW:
                                    #4/19 jmk creating a blank line: print_to_screen(dz_msg_screen) # could get overwritten in next section
                                    dz_msg_screen = "" # prevent duplicate printing below
                                # reset after 'monitored_playlist_cleared' to ensure 'song count' is available for it
                                reset_playlist_counts(found_playlist['name'] if found_playlist else "") 
                                count_overridden = False
                                
                                #jmkfix 2/28/2026
                                # # reset after 'monitored_playlist_cleared' to ensure 'song count' is available for it
                                # #jmkfix this will delete the dz_messages from _cleared call just above
                                # reset_playlist_counts(found_playlist['name'] if found_playlist else "") 
                                
                                #8/4/2025 fixed in reset_playlist_counts
                                # dz_message = ""
                            else:
                                # since haven't hit limit yet to consider playlist over, set found_playlist back to previous
                                found_playlist = last_found_playlist
                                # check to verify previous playlist was actually a confirmed playlist or counting up
                                if last_found_playlist['count_start'] >= last_found_playlist['qty_start']:
                                    is_playlist = True
                                    sp_playlist = found_playlist['name']
                                    sp_playlist_url = found_playlist.get('url', '')
                                    playlist_m_body = f"\nPlaylist: {sp_playlist}{iconstring()}"
                                    playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}</a>"
                                    found_playlist['count_shuffle'] += 1
                                    # don't show icon in this case, but OK to show playlist with an *
                                    # sp_track = sp_track + found_playlist.get('icon', '')
                                    if ALT_VIEW:
                                        icon_add = True
                                else:
                                    print_debug(f"SPECIAL CASE 2: PLAYLIST FOUND BUT PREVIOUS ONE WAS STILL COUNTING UP -> {found_playlist['name']}")

                                print_debug(f"HAVEN'T HIT LIMIT TO DISCONTINUE PLAYLIST (2) -> {found_playlist['name']}")
                        else:
                            reset_playlist_counts()
                            count_overridden = False
                            #8/4/2025 fixed in reset_playlist_counts
                            #dz_message = ""
                        # else:
                            # print_debug(f"INACTIVE USER, SKIPPING PLAYLIST CHECKS (2)")
                            #---
                    listened_songs += 1
        # print song line if NOT just becoming active
                    if not ((cur_ts - sp_ts_old) > SPOTIFY_INACTIVITY_CHECK and sp_active_ts_stop > 0):
        # main song line printer is here
                        if ALT_VIEW:
                            print_to_screen(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}")
                            send_notification(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}", sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '', time_diff_str(), listened_songs)
                            if dz_msg_screen:
                                print_debug(f"DZ_MSG_SCREEN: {dz_msg_screen}")
                                print_to_screen(dz_msg_screen)

                    print(f"Spotify user:\t\t\t{sp_username}")
                    print(f"\nLast played:\t\t\t{sp_artist} - {sp_track}")
                    print(f"Duration:\t\t\t{display_time(sp_track_duration)}")

                    # Suppress "Played for" if this track is the first after inactivity
                    cur_ts = int(time.time())
                    resumed_after_offline = (sp_active_ts_stop > 0) and ((cur_ts - sp_ts_old) > SPOTIFY_INACTIVITY_CHECK)
                    song_skipped = False
                    if not resumed_after_offline and (sp_ts - sp_ts_old) < (sp_track_duration - 1):
                        played_for_time = sp_ts - sp_ts_old
                        listened_percentage = (played_for_time) / (sp_track_duration - 1)
                        played_for = display_time(played_for_time)
                        percentage_display = int(listened_percentage * 100)

                        if listened_percentage <= SKIPPED_SONG_THRESHOLD:
                            played_for += f" - SKIPPED ({percentage_display}%)"
                            skipped_songs += 1
                            song_skipped = True
                        else:
                            # Check for potential crossfade (within detection thresholds, not skipped)
                            # Use displayed percentage for comparison to match what user sees
                            crossfade_note = ""
                            if DETECT_CROSSFADED_SONGS:
                                percentage_for_check = percentage_display / 100.0
                                if CROSSFADE_DETECTION_MIN <= percentage_for_check <= CROSSFADE_DETECTION_MAX:
                                    crossfade_note = " - crossfade enabled"
                            played_for += f" ({percentage_display}%{crossfade_note})"
                        print(f"Played for:\t\t\t{played_for}")
                        played_for_m_body = f"\nPlayed for: {played_for}"
                        played_for_m_body_html = f"<br>Played for: {played_for}"
                    elif not resumed_after_offline:
                        # Song played for full duration or longer (e.g. pause, ad etc.)
                        played_for_time = sp_ts - sp_ts_old
                        time_diff = abs(played_for_time - sp_track_duration)
                        if time_diff > PLAYED_FOR_DURATION_TOLERANCE:
                            # Song was played significantly longer or shorter than its duration
                            played_for = display_time(played_for_time)
                            print(f"Played for:\t\t\t{played_for}")
                            played_for_m_body = f"\nPlayed for: {played_for}"
                            played_for_m_body_html = f"<br>Played for: {played_for}"
                        else:
                            # Song played within tolerance of its duration (treat as full duration, suppress "Played for")
                            played_for_m_body = ""
                            played_for_m_body_html = ""
                    else:
                        # First track after inactivity: do not show "Played for" and never mark as skipped
                        played_for_m_body = ""
                        played_for_m_body_html = ""

                    # Add current song to recent songs session list
                    recent_songs_session.append({
                        'artist': sp_artist,
                        'track': sp_track,
                        'timestamp': sp_ts,
                        'skipped': song_skipped
                    })
                    # Keep only last INACTIVE_EMAIL_RECENT_SONGS_COUNT songs (or 5 if not set)
                    max_songs = INACTIVE_EMAIL_RECENT_SONGS_COUNT if INACTIVE_EMAIL_RECENT_SONGS_COUNT > 0 else 5
                    if len(recent_songs_session) > max_songs:
                        recent_songs_session.pop(0)

                    if is_playlist:
                        print(f"Playlist:\t\t\t{sp_playlist}{playlist_suffix}")

                    print(f"Album:\t\t\t\t{sp_album}")

                    context_m_body = ""
                    context_m_body_html = ""

#jmk                if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
                    if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
                        print(f"\nContext (Album):\t\t{sp_playlist}")
                        context_m_body += f"\nContext (Album): {sp_playlist}"
                        context_m_body_html += f"<br>Context (Album): <a href=\"{spotify_convert_uri_to_url(sp_playlist_uri)}\">{escape(sp_playlist)}</a>"

                    if 'spotify:artist:' in sp_playlist_uri:
                        print(f"\nContext (Artist):\t\t{sp_playlist}")
                        context_m_body += f"\nContext (Artist): {sp_playlist}"
                        context_m_body_html += f"<br>Context (Artist): <a href=\"{spotify_convert_uri_to_url(sp_playlist_uri)}\">{escape(sp_playlist)}</a>"

                    print(f"Last activity:\t\t\t{get_date_from_ts(sp_ts)}")

                    print(f"\nTrack URL:\t\t\t{sp_track_url}")
                    if is_playlist:
                        print(f"Playlist URL:\t\t\t{sp_playlist_url}")
                    print(f"Album URL:\t\t\t{sp_album_url}")

#jmk                if 'spotify:album:' in sp_playlist_uri and sp_playlist != sp_album:
                    if 'spotify:album:' in sp_playlist_uri and sp_playlist == sp_album:
                        print(f"Context (Album) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

                    if 'spotify:artist:' in sp_playlist_uri:
                        print(f"Context (Artist) URL:\t\t{spotify_convert_uri_to_url(sp_playlist_uri)}")

                    apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))

                    music_urls_output = format_music_urls_console(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                    if music_urls_output:
                        print(music_urls_output)
                    lyrics_output = format_lyrics_urls_console(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                    if lyrics_output:
                        print(lyrics_output)

                    if not is_playlist:
                        sp_playlist = ""

                    if song_on_loop == SONG_ON_LOOP_VALUE:
                        print("─" * HORIZONTAL_LINE)
                        print(f"User plays song on LOOP ({song_on_loop} times)")
                        print("─" * HORIZONTAL_LINE)

                    # Friend got active after being offline
                    if (cur_ts - sp_ts_old) > SPOTIFY_INACTIVITY_CHECK and sp_active_ts_stop > 0:
                        if JMK_MODE:
                            sp_active_ts_start = sp_ts # reset start time to [00] instead starting at length of the first song (ex:[04])
                        else:
                            sp_active_ts_start = sp_ts - sp_track_duration

                        listened_songs = 1
                        skipped_songs = 0
                        looped_songs = 0
                        song_on_loop = 1
                        recent_songs_session = [{'artist': sp_artist, 'track': sp_track, 'timestamp': sp_ts, 'skipped': False}]
                        active_ever = True
                        print_debug(f"ACTIVE EVER: {active_ever} (3)")

                        if FLAG_FILE:
                            flag_file_create()

                        print(f"\n*** Friend got ACTIVE after being offline for {calculate_timespan(int(sp_active_ts_start), int(sp_active_ts_stop))} ({get_date_from_ts(sp_active_ts_stop)})")
                        m_subject = f"Spotify user {sp_username} is active: '{sp_artist} - {sp_track}' (after {calculate_timespan(int(sp_active_ts_start), int(sp_active_ts_stop), show_seconds=False)} - {get_short_date_from_ts(sp_active_ts_stop)})"
                        friend_active_m_body = f"Friend got active after being offline for {calculate_timespan(int(sp_active_ts_start), int(sp_active_ts_stop))}\nLast activity (before getting offline): {get_date_from_ts(sp_active_ts_stop)}"
                        friend_active_m_body_html = f"Friend got active after being offline for <b>{calculate_timespan(int(sp_active_ts_start), int(sp_active_ts_stop))}</b><br>Last activity (before getting offline): <b>{get_date_from_ts(sp_active_ts_stop)}</b>"
                        if (sp_active_ts_start - sp_active_ts_stop) < 30:
                            listened_songs = listened_songs_old
                            skipped_songs = skipped_songs_old
                            looped_songs = looped_songs_old
                            print(f"*** Inactivity timer ({display_time(SPOTIFY_INACTIVITY_CHECK)}) value might be too low, readjusting session start back to {get_short_date_from_ts(sp_active_ts_start_old)}")
                            friend_active_m_body += f"\nInactivity timer ({display_time(SPOTIFY_INACTIVITY_CHECK)}) value might be too low, readjusting session start back to {get_short_date_from_ts(sp_active_ts_start_old)}"
                            friend_active_m_body_html += f"<br>Inactivity timer (<b>{display_time(SPOTIFY_INACTIVITY_CHECK)}</b>) value might be <b>too low</b>, readjusting session start back to <b>{get_short_date_from_ts(sp_active_ts_start_old)}</b>"
                            if sp_active_ts_start_old > 0:
                                sp_active_ts_start = sp_active_ts_start_old
                        sp_active_ts_stop = 0

                        print_debug(f"LOOP C - FOR ALL SONGS - FRIEND ACTIVE AFTER BEING OFFLINE")
                        if ALT_VIEW:
#                            song_count = 1
                            print_to_screen(f" ")
                            print_to_screen(f"----------------------")
#                            print_to_both(f"{timestring()}: {ERR_CODE}, *** Start text sent. Track: {songstring()}")
                            print_to_both(f"{timestring()}: {ERR_CODE}, *** Start notification sent")
# this is executed when friend becomes active
# already handled above for every song (2), THEN this (3) gets executed for the 'got ACTIVE' messaging
                            # #---
                            # dz_msg_screen = ""
                            # dz_str = f"{sp_artist} - {sp_track}"
                            
                            # 8/5 uncommented to ensure refresh of foound_playlist
                            last_found_playlist = found_playlist
                            if not hasTrack and (sp_playlist_owner != "Spotify"):
                                found_playlist = find_song_in_playlists(dz_str, found_playlist, sp_playlist if is_playlist else "")
                            else:
                                found_playlist = False
                                last_found_playlist = False
                                print_debug(f"SKIPPED FIND_SONG_IN_PLAYLIST (3) -> hasTrack: {hasTrack}")                   

                            if found_playlist:
                                print_debug(f"FOUND PLAYLIST IN MONITORING LIST (3) -> {found_playlist['name']}")
                                print_debug(f"COUNT START: {found_playlist['count_start']}, {found_playlist['qty_start']}")
# already handled above for every song (2), THEN this (3) gets executed for the 'got ACTIVE' messaging
# so this +1 is extra and double-counts
                                # save_count = found_playlist['count_start']
                                # reset_playlist_counts()
                                # found_playlist['count_start'] = save_count + 1
                                # print_debug(f"COUNT START + 1: {found_playlist['count_start']}")

                                # don't check to override count here; only do it when starting up, not when user starts back up later
                                # count was high enough to trigger detection
# already handled above for every song (2), THEN this (3) gets executed for the 'got ACTIVE' messaging
# so this is redundant
                                # this is needed to cause detection messaging/notifications when user becomes active and already on a detected playlist
                                if found_playlist['count_start'] >= found_playlist['qty_start']:
                                    print_debug(f"PLAYLIST_DETECTED (3): {found_playlist['count_start']}, {found_playlist['qty_start']}")
                                    is_playlist = True
                                    sp_playlist = found_playlist['name']
                                    sp_playlist_url = found_playlist.get('url', '')
                                    playlist_m_body = f"\nPlaylist: {sp_playlist}{iconstring()}"
                                    playlist_m_body_html = f"<br>Playlist: <a href=\"{sp_playlist_url}\">{escape(sp_playlist)}</a>"
                                    save_track = sp_track
                                    sp_track = sp_track + found_playlist.get('icon', '')
                                    body_dz, body_dz_html, dz_message, dz_msg_screen = monitored_playlist_detected(found_playlist, songstring(), time_diff_str(), True, sp_track, sp_artist, sp_album)
                                    # restore to avoid adding 'icon' twice (in code processing all tracks)
                                    sp_track = save_track
                                # else:
                                    # dz_message = build_dz_string(found_playlist)
                                    # if DEBUG_JMK and dz_message != "":
                                        # dz_message = dz_message + " (5)"
                            # else:
                                # reset_playlist_counts()

                                # process a possible exception if last song was in a playlist (even if as exception) AND it's an active playlist (not counting up towards it)
                                # actually, if not allowing exception during counting up to > 2, may never get there since smart shuffle puts a new song every 3
                                # if last_found_playlist and (last_found_playlist['count_start'] >= last_found_playlist['qty_start']):
                                # if last_found_playlist:
                                    # print_debug(f"COUNT END: {last_found_playlist['count_end']}")
                                    # last_found_playlist['count_end'] += 1
                                    # print_debug(f"COUNT END + 1: {last_found_playlist['count_end']}")
                                    # if last_found_playlist['count_end'] >= last_found_playlist['qty_end']:
                                        # # limit achieved
                                        # # reset_playlist_counts()
                                        # dz_message, dz_msg_screen = monitored_playlist_cleared(last_found_playlist, songstring(), time_diff_str())
                                    # else:
                                        # # since haven't hit limit yet to consider playlist over, set found_playlist back to previous
                                        # found_playlist = last_found_playlist
                                        # is_playlist = True
                                        # sp_playlist = found_playlist['name']
                                        # sp_playlist_url = found_playlist.get('url', '')
                                        # # don't show icon in this case, but OK to show playlist with an *
                                        # # sp_track = sp_track + found_playlist.get('icon', '')
                                        # if ALT_VIEW:
                                            # icon_add = True
                                        # print_debug(f"HAVEN'T HIT LIMIT TO DISCONTINUE PLAYLIST (3) -> {found_playlist['name']}")
                                # # else:
                                    # reset_playlist_counts()

                            #---
                            print_to_screen(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}")
                            send_notification(f"{timestring()}: {ERR_CODE}, [{time_diff_str()}] {songstring()}", sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '', time_diff_str(), listened_songs)
                            if SEND_NOTIFY:
                                # send_notification(f"START: {songstring()}", sp_album_image_url)
                                send_notification(f"START: {songstring()}", sp_playlist_image_url if sp_playlist_image_url else sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '')
                             
                        music_urls_text = format_music_urls_email_text(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                        music_urls_html = format_music_urls_email_html(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url, sp_artist, sp_track)
                        lyrics_urls_text = format_lyrics_urls_email_text(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                        lyrics_urls_html = format_lyrics_urls_email_html(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, sp_artist, sp_track)
                        if music_urls_text:
                            music_section_text = f"\n\n{music_urls_text}"
                            music_section_html = f"<br><br>{music_urls_html}"
                            lyrics_section_text = f"\n{lyrics_urls_text}\n\n" if lyrics_urls_text else "\n\n"
                            lyrics_section_html = f"<br>{lyrics_urls_html}<br><br>" if lyrics_urls_html else "<br><br>"
                        else:
                            if lyrics_urls_text:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = f"{lyrics_urls_text}\n\n"
                                lyrics_section_html = f"{lyrics_urls_html}<br><br>"
                            else:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = ""
                                lyrics_section_html = ""
                        m_body = f"Last played: {sp_artist} - {sp_track}\nDuration: {display_time(sp_track_duration)}{played_for_m_body}{playlist_m_body}\nAlbum: {sp_album}{context_m_body}{music_section_text}{lyrics_section_text}{friend_active_m_body}\n\nSongs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})\n\nLast activity: {get_date_from_ts(sp_ts)}{get_cur_ts(nl_ch + 'Timestamp: ')}"
                        m_body_html = f"<html><head></head><body>Last played: <b><a href=\"{sp_artist_url}\">{escape(sp_artist)}</a> - <a href=\"{sp_track_url}\">{escape(sp_track)}</a></b><br>Duration: {display_time(sp_track_duration)}{played_for_m_body_html}{playlist_m_body_html}<br>Album: <a href=\"{sp_album_url}\">{escape(sp_album)}</a>{context_m_body_html}{music_section_html}{lyrics_section_html}{friend_active_m_body_html}<br><br>Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})<br><br>Last activity: {get_date_from_ts(sp_ts)}{get_cur_ts('<br>Timestamp: ')}</body></html>"

                        active_ever = True
                        if ACTIVE_NOTIFICATION:
                            print(f"Sending email notification to {RECEIVER_EMAIL}")
                            email_sent = True
                            if JMK_MODE:
                                song_footer_txt, song_footer_html = update_spreadsheet_row(f"{datetime.now().strftime('%H:%M:%S')} {songstring()}", True)
                                m_body += song_footer_txt
                                m_body_html = m_body_html.replace("</body></html>", song_footer_html + "</body></html>")
                            if not JMK_MODE or ORIG_EMAILS:
                                send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                            if JMK_MODE:
                                update_spreadsheet_row(SPREADSHEET_DIVIDER_TEXT, False)
                                send_email(f"{GMAIL_TAG}---------------------------------", "  ", "  ", SMTP_SSL)
                                send_email(f"{GMAIL_TAG}[{time_diff_str()}] {timestring()} {songstring()}", m_body, m_body_html, SMTP_SSL)

                    on_the_list = False
                    if sp_track.upper() in tracks_upper or sp_playlist.upper() in tracks_upper or sp_album.upper() in tracks_upper:
                        print("\n*** Track/playlist/album matched with the list!")
                        on_the_list = True

                    # Check for loop notification first - if sent, skip track/song notification
                    if song_on_loop == SONG_ON_LOOP_VALUE and SONG_ON_LOOP_NOTIFICATION and not email_sent:
                        music_urls_text = format_music_urls_email_text(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                        music_urls_html = format_music_urls_email_html(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url, sp_artist, sp_track)
                        lyrics_urls_text = format_lyrics_urls_email_text(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                        lyrics_urls_html = format_lyrics_urls_email_html(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, sp_artist, sp_track)
                        if music_urls_text:
                            music_section_text = f"\n\n{music_urls_text}"
                            music_section_html = f"<br><br>{music_urls_html}"
                            lyrics_section_text = f"\n{lyrics_urls_text}\n\n" if lyrics_urls_text else "\n\n"
                            lyrics_section_html = f"<br>{lyrics_urls_html}<br><br>" if lyrics_urls_html else "<br><br>"
                        else:
                            if lyrics_urls_text:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = f"{lyrics_urls_text}\n\n"
                                lyrics_section_html = f"{lyrics_urls_html}<br><br>"
                            else:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = ""
                                lyrics_section_html = ""
                        m_subject = f"Spotify user {sp_username} plays song on loop: '{sp_artist} - {sp_track}'"
                        m_body = f"Last played: {sp_artist} - {sp_track}\nDuration: {display_time(sp_track_duration)}{played_for_m_body}{playlist_m_body}\nAlbum: {sp_album}{context_m_body}{music_section_text}{lyrics_section_text}User plays song on LOOP ({song_on_loop} times)\n\nSongs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})\n\nLast activity: {get_date_from_ts(sp_ts)}{get_cur_ts(nl_ch + 'Timestamp: ')}"
                        m_body_html = f"<html><head></head><body>Last played: <b><a href=\"{sp_artist_url}\">{escape(sp_artist)}</a> - <a href=\"{sp_track_url}\">{escape(sp_track)}</a></b><br>Duration: {display_time(sp_track_duration)}{played_for_m_body_html}{playlist_m_body_html}<br>Album: <a href=\"{sp_album_url}\">{escape(sp_album)}</a>{context_m_body_html}{music_section_html}{lyrics_section_html}User plays song on LOOP (<b>{song_on_loop}</b> times)<br><br>Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})<br><br>Last activity: {get_date_from_ts(sp_ts)}{get_cur_ts('<br>Timestamp: ')}</body></html>"
                        print(f"Sending email notification to {RECEIVER_EMAIL}")
                        send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                        email_sent = True

                    if (TRACK_NOTIFICATION and on_the_list and not email_sent) or (SONG_NOTIFICATION and not email_sent):
                        music_urls_text = format_music_urls_email_text(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                        music_urls_html = format_music_urls_email_html(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url, sp_artist, sp_track)
                        lyrics_urls_text = format_lyrics_urls_email_text(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                        lyrics_urls_html = format_lyrics_urls_email_html(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, sp_artist, sp_track)
                        if music_urls_text:
                            music_section_text = f"\n\n{music_urls_text}"
                            music_section_html = f"<br><br>{music_urls_html}"
                            lyrics_section_text = f"\n{lyrics_urls_text}\n\n" if lyrics_urls_text else "\n\n"
                            lyrics_section_html = f"<br>{lyrics_urls_html}<br><br>" if lyrics_urls_html else "<br><br>"
                        else:
                            if lyrics_urls_text:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = f"{lyrics_urls_text}\n\n"
                                lyrics_section_html = f"{lyrics_urls_html}<br><br>"
                            else:
                                music_section_text = "\n\n"
                                music_section_html = "<br><br>"
                                lyrics_section_text = ""
                                lyrics_section_html = ""
                        m_subject = f"Spotify user {sp_username}: '{sp_artist} - {sp_track}'"
                        m_body = f"Last played: {sp_artist} - {sp_track}\nDuration: {display_time(sp_track_duration)}{played_for_m_body}{playlist_m_body}\nAlbum: {sp_album}{context_m_body}{music_section_text}{lyrics_section_text}Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})\n{body_dz}Last activity: {get_date_from_ts(sp_ts)}{get_cur_ts(nl_ch + 'Timestamp: ')}"
                        m_body_html = f"<html><head></head><body>Last played: <b><a href=\"{sp_artist_url}\">{escape(sp_artist)}</a> - <a href=\"{sp_track_url}\">{escape(sp_track)}</a></b><br>Duration: {display_time(sp_track_duration)}{played_for_m_body_html}{playlist_m_body_html}<br>Album: <a href=\"{sp_album_url}\">{escape(sp_album)}</a>{context_m_body_html}{music_section_html}{lyrics_section_html}Songs played: {listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})<br>{body_dz_html}Last activity: {get_date_from_ts(sp_ts)}{get_cur_ts('<br>Timestamp: ')}</body></html>"
                        print(f"Sending email notification to {RECEIVER_EMAIL}")
                        email_sent = True
                        if JMK_MODE:
                            song_footer_txt, song_footer_html = update_spreadsheet_row(f"{datetime.now().strftime('%H:%M:%S')} {songstring()}", True)
                            m_body += song_footer_txt
                            m_body_html = m_body_html.replace("</body></html>", song_footer_html + "</body></html>")
                            send_email(f"{GMAIL_TAG}[{time_diff_str()}] {timestring()} {songstring()}", m_body, m_body_html, SMTP_SSL)
                        if not JMK_MODE or ORIG_EMAILS:
                            send_email(m_subject, m_body, m_body_html, SMTP_SSL)

                    try:
                        if csv_file_name:
                            write_csv_entry(csv_file_name, datetime.fromtimestamp(int(cur_ts)), sp_artist, sp_track, sp_playlist, sp_album, datetime.fromtimestamp(int(sp_ts)))
                    except Exception as e:
                        print(f"* Error: {e}")

                    if dz_message or listened_songs:
                        print("")
                    if dz_message:
                        print(dz_message)
                    if listened_songs:
                        print(f"Songs played:\t\t\t{listened_songs} ({calculate_timespan(int(sp_ts), int(sp_active_ts_start))})")
                    if ALT_VIEW:
                        icon_add = False
                    hastrack = False
                    
                    print_cur_ts("\nTimestamp:\t\t\t")
                    sp_ts_old = sp_ts
                # Track has not changed
                else:
                    # Removed because it happens every 9 minutes (timeout)
                    # print_debug(f"LOOP C - FOR ALL SONGS - SONG HAS NOT CHANGED")
                    alive_counter += 1
                    # Friend got inactive
                    if (cur_ts - sp_ts) > SPOTIFY_INACTIVITY_CHECK and sp_active_ts_start > 0:
                        sp_active_ts_stop = sp_ts
                        print(f"*** Friend got INACTIVE after listening to music for {calculate_timespan(int(sp_active_ts_stop), int(sp_active_ts_start))}")
                        print(f"*** Friend played music from {get_range_of_dates_from_tss(sp_active_ts_start, sp_active_ts_stop, short=True, between_sep=' to ')}")

                        if FLAG_FILE:
                            flag_file_delete()

                        listened_songs_text = f"*** User played {listened_songs} songs"
                        listened_songs_mbody = f"\n\nUser played {listened_songs} songs"
                        listened_songs_mbody_html = f"<br><br>User played <b>{listened_songs}</b> songs"

                        if skipped_songs > 0:
                            skipped_songs_text = f", skipped {skipped_songs} songs ({int((skipped_songs / listened_songs) * 100)}%)"
                            listened_songs_text += skipped_songs_text
                            listened_songs_mbody += skipped_songs_text
                            listened_songs_mbody_html += f", skipped <b>{skipped_songs}</b> songs <b>({int((skipped_songs / listened_songs) * 100)}%)</b>"

                        if looped_songs > 0:
                            looped_songs_text = f"\n*** User played {looped_songs} songs on loop"
                            looped_songs_mbody = f"\nUser played {looped_songs} songs on loop"
                            looped_songs_mbody_html = f"<br>User played <b>{looped_songs}</b> songs on loop"
                            listened_songs_text += looped_songs_text
                            listened_songs_mbody += looped_songs_mbody
                            listened_songs_mbody_html += looped_songs_mbody_html

                        if is_playlist:
                            playlist_suffix = SPOTIFY_SUFFIX if sp_playlist_owner == "Spotify" else ""
                            playlist_suffix += (ICON_SONG_MISSING_FROM_PLAYLIST if icon_add else "")

                        if JMK_MODE:
                            print_to_both(f"{timestring()}: {ERR_CODE}, *** End notification sent")
                            if SEND_NOTIFY:
                                # send_notification(f"END: [{time_diff_str()}]: {songstring()}, Song Count: {listened_songs}", sp_album_image_url)
                                send_notification(f"END: [{time_diff_str()}]: {songstring()}, Song Count: {listened_songs}", sp_playlist_image_url if sp_playlist_image_url else sp_album_image_url, sp_track, sp_artist, sp_album, (sp_playlist+iconstring()) if is_playlist else '', time_diff_str(), listened_songs)

                        print(listened_songs_text)

                        print(f"*** Last activity:\t\t{get_date_from_ts(sp_active_ts_stop)} (inactive timer: {display_time(SPOTIFY_INACTIVITY_CHECK)})")
                        # If tracking functionality is enabled then either pause the current song via Spotify client or play the indicated SP_USER_GOT_OFFLINE_TRACK_ID "finishing" song
                        if TRACK_SONGS:
                            if SP_USER_GOT_OFFLINE_TRACK_ID:
                                if platform.system() == 'Darwin':       # macOS
                                    spotify_macos_play_song(SP_USER_GOT_OFFLINE_TRACK_ID)
                                    if SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE > 0:
                                        time.sleep(SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE)
                                        spotify_macos_play_pause("pause")
                                elif platform.system() == 'Windows':    # Windows
                                    pass
                                else:                                   # Linux variants
                                    spotify_linux_play_song(SP_USER_GOT_OFFLINE_TRACK_ID)
                                    if SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE > 0:
                                        time.sleep(SP_USER_GOT_OFFLINE_DELAY_BEFORE_PAUSE)
                                        spotify_linux_play_pause("pause")
                            else:
                                if platform.system() == 'Darwin':       # macOS
                                    spotify_macos_play_pause("pause")
                                elif platform.system() == 'Windows':    # Windows
                                    pass
                                else:                                   # Linux variants
                                    spotify_linux_play_pause("pause")
                        if INACTIVE_NOTIFICATION:
                            # Format recently listened songs list for email (skip if only 1 song)
                            recent_songs_mbody = ""
                            recent_songs_mbody_html = ""
                            if listened_songs > 1 and len(recent_songs_session) > 0 and INACTIVE_EMAIL_RECENT_SONGS_COUNT > 0:
                                # Get last up to INACTIVE_EMAIL_RECENT_SONGS_COUNT songs
                                songs_to_show = recent_songs_session[-min(INACTIVE_EMAIL_RECENT_SONGS_COUNT, len(recent_songs_session)):]
                                recent_songs_list = []
                                recent_songs_list_html = []
                                for song in songs_to_show:
                                    song_date = get_date_from_ts(song['timestamp'])
                                    skipped_text = ", SKIPPED" if song.get('skipped', False) else ""
                                    recent_songs_list.append(f"{song['artist']} - {song['track']} ({song_date}{skipped_text})")
                                    skipped_html = ", <b>SKIPPED</b>" if song.get('skipped', False) else ""
                                    recent_songs_list_html.append(f"<b>{escape(song['artist'])} - {escape(song['track'])}</b> ({song_date}{skipped_html})")
                                if recent_songs_list:
                                    recent_songs_mbody = f"\n\nRecently listened songs in this session:\n" + "\n".join(recent_songs_list)
                                    recent_songs_mbody_html = f"<br><br>Recently listened songs in this session:<br>" + "<br>".join(recent_songs_list_html)

                            # Get URLs for the last played track
                            apple_search_url, genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url = get_apple_genius_search_urls(str(sp_artist), str(sp_track))
                            music_urls_text = format_music_urls_email_text(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url)
                            music_urls_html = format_music_urls_email_html(apple_search_url, youtube_music_search_url, amazon_music_search_url, deezer_search_url, tidal_search_url, sp_artist, sp_track)
                            lyrics_urls_text = format_lyrics_urls_email_text(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url)
                            lyrics_urls_html = format_lyrics_urls_email_html(genius_search_url, azlyrics_search_url, tekstowo_search_url, musixmatch_search_url, lyrics_com_search_url, sp_artist, sp_track)
                            if music_urls_text:
                                music_section_text = f"\n\n{music_urls_text}"
                                music_section_html = f"<br><br>{music_urls_html}"
                                lyrics_section_text = f"\n{lyrics_urls_text}\n\n" if lyrics_urls_text else "\n\n"
                                lyrics_section_html = f"<br>{lyrics_urls_html}<br><br>" if lyrics_urls_html else "<br><br>"
                            else:
                                if lyrics_urls_text:
                                    music_section_text = "\n\n"
                                    music_section_html = "<br><br>"
                                    lyrics_section_text = f"{lyrics_urls_text}\n\n"
                                    lyrics_section_html = f"{lyrics_urls_html}<br><br>"
                                else:
                                    music_section_text = "\n\n"
                                    music_section_html = "<br><br>"
                                    lyrics_section_text = ""
                                    lyrics_section_html = ""
                            m_subject = f"Spotify user {sp_username} is inactive: '{sp_artist} - {sp_track}' (after {calculate_timespan(int(sp_active_ts_stop), int(sp_active_ts_start), show_seconds=False)}: {get_range_of_dates_from_tss(sp_active_ts_start, sp_active_ts_stop, short=True)})"
                            m_body = f"Last played: {sp_artist} - {sp_track}\nDuration: {display_time(sp_track_duration)}{played_for_m_body}{playlist_m_body}\nAlbum: {sp_album}{context_m_body}{music_section_text}{lyrics_section_text}Friend got inactive after listening to music for {calculate_timespan(int(sp_active_ts_stop), int(sp_active_ts_start))}\nFriend played music from {get_range_of_dates_from_tss(sp_active_ts_start, sp_active_ts_stop, short=True, between_sep=' to ')}{listened_songs_mbody}{recent_songs_mbody}\n{body_dz}Last activity: {get_date_from_ts(sp_active_ts_stop)}\nInactivity timer: {display_time(SPOTIFY_INACTIVITY_CHECK)}{get_cur_ts(nl_ch + 'Timestamp: ')}"
                            m_body_html = f"<html><head></head><body>Last played: <b><a href=\"{sp_artist_url}\">{escape(sp_artist)}</a> - <a href=\"{sp_track_url}\">{escape(sp_track)}</a></b><br>Duration: {display_time(sp_track_duration)}{played_for_m_body_html}{playlist_m_body_html}<br>Album: <a href=\"{sp_album_url}\">{escape(sp_album)}</a>{context_m_body_html}{music_section_html}{lyrics_section_html}Friend got inactive after listening to music for <b>{calculate_timespan(int(sp_active_ts_stop), int(sp_active_ts_start))}</b><br>Friend played music from <b>{get_range_of_dates_from_tss(sp_active_ts_start, sp_active_ts_stop, short=True, between_sep='</b> to <b>')}</b>{listened_songs_mbody_html}{recent_songs_mbody_html}<br>{body_dz_html}Last activity: <b>{get_date_from_ts(sp_active_ts_stop)}</b><br>Inactivity timer: {display_time(SPOTIFY_INACTIVITY_CHECK)}{get_cur_ts('<br>Timestamp: ')}</body></html>"
                            print(f"Sending email notification to {RECEIVER_EMAIL}")
                            send_email(m_subject, m_body, m_body_html, SMTP_SSL)
                            email_sent = True
                        sp_active_ts_start_old = sp_active_ts_start
                        sp_active_ts_start = 0
                        listened_songs_old = listened_songs
                        skipped_songs_old = skipped_songs
                        looped_songs_old = looped_songs
                        listened_songs = 0
                        looped_songs = 0
                        skipped_songs = 0
                        song_on_loop = 0
                        recent_songs_session = []
                        print_cur_ts("\nTimestamp:\t\t\t")

                    if LIVENESS_CHECK_COUNTER and alive_counter >= LIVENESS_CHECK_COUNTER:
                        print_cur_ts("Liveness check, timestamp:\t")
                        alive_counter = 0

                time.sleep(SPOTIFY_CHECK_INTERVAL)

                ERROR_500_ZERO_TIME_LIMIT = ERROR_500_TIME_LIMIT + SPOTIFY_CHECK_INTERVAL
                if SPOTIFY_CHECK_INTERVAL * ERROR_500_NUMBER_LIMIT > ERROR_500_ZERO_TIME_LIMIT:
                    ERROR_500_ZERO_TIME_LIMIT = SPOTIFY_CHECK_INTERVAL * (ERROR_500_NUMBER_LIMIT + 1)

                if error_500_start_ts and ((int(time.time()) - error_500_start_ts) >= ERROR_500_ZERO_TIME_LIMIT):
                    error_500_start_ts = 0
                    error_500_counter = 0

                ERROR_NETWORK_ZERO_TIME_LIMIT = ERROR_NETWORK_ISSUES_TIME_LIMIT + SPOTIFY_CHECK_INTERVAL
                if SPOTIFY_CHECK_INTERVAL * ERROR_NETWORK_ISSUES_NUMBER_LIMIT > ERROR_NETWORK_ZERO_TIME_LIMIT:
                    ERROR_NETWORK_ZERO_TIME_LIMIT = SPOTIFY_CHECK_INTERVAL * (ERROR_NETWORK_ISSUES_NUMBER_LIMIT + 1)

                if error_network_issue_start_ts and ((int(time.time()) - error_network_issue_start_ts) >= ERROR_NETWORK_ZERO_TIME_LIMIT):
                    error_network_issue_start_ts = 0
                    error_network_issue_counter = 0

        # User is not found in the Spotify's friend list just after starting the tool
        else:
            if user_not_found is False:
                if is_user_removed(sp_accessToken_oauth_app, user_uri_id, oauth_app=True):
                    print(f"User '{user_uri_id}' does not exist! Retrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals")
                else:
                    print(f"User '{user_uri_id}' not found - make sure your friend is followed and has activity sharing enabled. Retrying in {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)} intervals")
                print_cur_ts("Timestamp:\t\t\t")
                user_not_found = True
            time.sleep(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)
            continue


def main():
    global CLI_CONFIG_PATH, DOTENV_FILE, LIVENESS_CHECK_COUNTER, LOGIN_REQUEST_BODY_FILE, CLIENTTOKEN_REQUEST_BODY_FILE, REFRESH_TOKEN, LOGIN_URL, USER_AGENT, DEVICE_ID, SYSTEM_ID, USER_URI_ID, SP_DC_COOKIE, CSV_FILE, MONITOR_LIST_FILE, FILE_SUFFIX, DISABLE_LOGGING, DEBUG_MODE, SP_LOGFILE, ACTIVE_NOTIFICATION, INACTIVE_NOTIFICATION, TRACK_NOTIFICATION, SONG_NOTIFICATION, SONG_ON_LOOP_NOTIFICATION, ERROR_NOTIFICATION, SPOTIFY_CHECK_INTERVAL, SPOTIFY_INACTIVITY_CHECK, SPOTIFY_ERROR_INTERVAL, SPOTIFY_DISAPPEARED_CHECK_INTERVAL, TRACK_SONGS, SMTP_PASSWORD, stdout_bck, APP_VERSION, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR, CLIENT_MODEL, TOKEN_SOURCE, ALARM_TIMEOUT, pyotp, USER_AGENT, FLAG_FILE, TRUNCATE_CHARS, SP_APP_TOKENS_FILE, SP_APP_CLIENT_ID, SP_APP_CLIENT_SECRET
    global ALT_VIEW, JMK_MODE, INITIAL_STARTUP, GMAIL_TAG, ERR_CODE, SEND_NOTIFY, DZ_ALERTS, ORIG_EMAILS, USER_ID, ALT_COOKIE, ADD_PLAYLISTS_TO_MONITOR, DEBUG_JMK, UPDATE_SPREADSHEET
    global FINAL_LOG_PATH, log_logger

    log_logger = None  # Initialize to None

#    global log_logger, screen_logger, both_logger, FINAL_LOG_PATH

    if "--generate-config" in sys.argv:
        config_content = CONFIG_BLOCK.strip("\n") + "\n"
        # Check if a filename was provided after --generate-config
        try:
            idx = sys.argv.index("--generate-config")
            if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("-"):
                # Write directly to file (bypasses PowerShell UTF-16 encoding issue on Windows)
                output_file = sys.argv[idx + 1]
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(config_content)
                print(f"Config written to: {output_file}")
                sys.exit(0)
        except (ValueError, IndexError):
            pass
        # No filename provided - write to stdout using buffer to ensure UTF-8
        sys.stdout.buffer.write(config_content.encode("utf-8"))
        sys.stdout.buffer.flush()
        sys.exit(0)

    if "--version" in sys.argv:
        print(f"{os.path.basename(sys.argv[0])} v{VERSION}")
        sys.exit(0)

    stdout_bck = sys.stdout

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    clear_screen(CLEAR_SCREEN)

    print(f"Spotify Monitoring Tool v{VERSION}\n")

    parser = argparse.ArgumentParser(
        prog="spotify_monitor",
        description=("Monitor a Spotify friend's activity and send customizable email alerts [ https://github.com/misiektoja/spotify_monitor/ ]"), formatter_class=argparse.RawTextHelpFormatter
    )

    # Positional
    parser.add_argument(
        "user_id",
        nargs="?",
        metavar="SPOTIFY_USER_URI_ID",
        help="Spotify user URI ID",
        type=str
    )

    # Version, just to list in help, it is handled earlier
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{VERSION}"
    )

    # Configuration & dotenv files
    conf = parser.add_argument_group("Configuration & dotenv files")
    conf.add_argument(
        "--config-file",
        dest="config_file",
        metavar="PATH",
        help="Location of the optional config file",
    )
    conf.add_argument(
        "--generate-config",
        dest="generate_config",
        nargs="?",
        const=True,
        metavar="FILENAME",
        help="Print default config template and exit (on Windows PowerShell, specify a filename to avoid redirect encoding issues)",
    )
    conf.add_argument(
        "--env-file",
        dest="env_file",
        metavar="PATH",
        help="Path to optional dotenv file (auto-search if not set, disable with 'none')",
    )

    # Token source
    parser.add_argument(
        "--token-source",
        dest="token_source",
        choices=["cookie", "client"],
        help="Method to obtain Spotify access token: 'cookie' (via sp_dc cookie) or 'client' (via desktop client login protobuf)"
    )

    # Auth details used when token source is set to cookie
    cookie_auth = parser.add_argument_group("Auth details for 'cookie' token source")
    cookie_auth.add_argument(
        "-u", "--spotify-dc-cookie",
        dest="spotify_dc_cookie",
        metavar="SP_DC_COOKIE",
        type=str,
        help="Spotify sp_dc cookie"
    )
    cookie_auth.add_argument(
        "-f", "--alt-cookie",
        dest="alt_cookie",
        action="store_true",
        help="Use secondary sp_dc cookie (SP_DC_COOKIE2) and Client protobuf (LOGIN_REQUEST_BODY_FILE2)"
    )

    # Auth details used when token source is set to client
    client_auth = parser.add_argument_group("Auth details for 'client' token source")
    client_auth.add_argument(
        "-w", "--login-request-body-file",
        dest="login_request_body_file",
        metavar="PROTOBUF_FILENAME",
        help="Read device_id, system_id, user_uri_id and refresh_token from binary Protobuf login file"
    )

    client_auth.add_argument(
        "-z", "--clienttoken-request-body-file",
        dest="clienttoken_request_body_file",
        metavar="PROTOBUF_FILENAME",
        # help="Read app_version, cpu_arch, os_build, platform, os_major, os_minor and client_model from binary Protobuf client token file"
        help=argparse.SUPPRESS
    )

    # OAuth app credentials (Client Credentials Flow) for track/user API calls, required for both cookie and client token sources
    oauth_app_auth = parser.add_argument_group("OAuth app credentials for track/user API calls")
    oauth_app_auth.add_argument(
        "-r", "--oauth-app-creds",
        dest="oauth_app_creds",
        metavar='SPOTIFY_APP_CLIENT_ID:SPOTIFY_APP_CLIENT_SECRET',
        help="Spotify OAuth app client credentials - specify both values as SPOTIFY_APP_CLIENT_ID:SPOTIFY_APP_CLIENT_SECRET"
    )

    # Notifications
    notify = parser.add_argument_group("Notifications")
    notify.add_argument(
        "-a", "--notify-active",
        dest="notify_active",
        action="store_true",
        default=None,
        help="Email when user becomes active"
    )
    notify.add_argument(
        "-i", "--notify-inactive",
        dest="notify_inactive",
        action="store_true",
        default=None,
        help="Email when user goes inactive"
    )
    notify.add_argument(
        "-t", "--notify-track",
        dest="notify_track",
        action="store_true",
        default=None,
        help="Email when a monitored track/playlist/album plays"
    )
    notify.add_argument(
        "-j", "--notify-song-changes",
        dest="notify_song_changes",
        action="store_true",
        default=None,
        help="Email on every song change"
    )
    notify.add_argument(
        "-x", "--notify-loop",
        dest="notify_loop",
        action="store_true",
        default=None,
        help="Email when user plays a song on loop"
    )
    notify.add_argument(
        "-e", "--no-error-notify",
        dest="notify_errors",
        action="store_false",
        default=None,
        help="Disable emails on errors"
    )
    notify.add_argument(
        "--send-test-email",
        dest="send_test_email",
        action="store_true",
        help="Send test email to verify SMTP settings"
    )

    # Intervals & timers
    times = parser.add_argument_group("Intervals & timers")
    times.add_argument(
        "-c", "--check-interval",
        dest="check_interval",
        metavar="SECONDS",
        type=int,
        help="Time between monitoring checks, in seconds"
    )
    times.add_argument(
        "-o", "--offline-timer",
        dest="offline_timer",
        metavar="SECONDS",
        type=int,
        help="Time required to mark inactive user as offline, in seconds"
    )
    times.add_argument(
        "-m", "--disappeared-timer",
        dest="disappeared_timer",
        metavar="SECONDS",
        type=int,
        help="Wait time between checks once the user disappears from friends list, in seconds"
    )

    # Listing
    listing = parser.add_argument_group("Listing")
    listing.add_argument(
        "-l", "--list-friends",
        dest="list_friends",
        action="store_true",
        help="List Spotify friends with their last listened track"
    )

    # Features & output
    opts = parser.add_argument_group("Features & output")
    opts.add_argument(
        "-g", "--track-in-spotify",
        dest="track_in_spotify",
        action="store_true",
        default=None,
        help="Auto-play each listened song in your Spotify client"
    )
    opts.add_argument(
        "-b", "--csv-file",
        dest="csv_file",
        metavar="CSV_FILE",
        type=str,
        help="Write every listened track to CSV file"
    )
    opts.add_argument(
        "-s", "--monitor-list",
        dest="monitor_list",
        metavar="TRACKS_FILE",
        type=str,
        help="Filename with Spotify tracks/playlists/albums to alert on"
    )
    opts.add_argument(
        "--flag-file",
        dest="flag_file",
        metavar="PATH",
        help="Path to flag file that is created when the user is active and deleted when inactive",
    )
    opts.add_argument(
        "--user-agent",
        dest="user_agent",
        metavar="USER_AGENT",
        type=str,
        help="Specify a custom user agent for Spotify API requests; leave empty to auto-generate it"
    )
    opts.add_argument(
        "-y", "--file-suffix",
        dest="file_suffix",
        metavar="SUFFIX",
        type=str,
        help="File suffix to append to output filenames instead of Spotify user URI ID"
    )
    opts.add_argument(
        "-d", "--disable-logging",
        dest="disable_logging",
        action="store_true",
        default=None,
        help="Disable logging to spotify_monitor_<user_uri_id/file_suffix>.log"
    )
    opts.add_argument(
        "--debug",
        dest="debug_mode",
        action="store_true",
        default=None,
        help="Enable debug mode for technical logging"
    )
    opts.add_argument(
        "--truncate",
        dest="truncate",
        metavar="N",
        type=int,
        help="Max characters per screen line (not log), use 999 to auto-detect terminal width, ignored if -d is set"
    )
    opts.add_argument(
        "-k", "--jmk",
        dest="jmk",
        action="store_true",
        default=None,
        help="Enable Jeoff's view and turn on texting"
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.config_file:
        CLI_CONFIG_PATH = os.path.expanduser(args.config_file)

    cfg_path = find_config_file(CLI_CONFIG_PATH)

    if not cfg_path and CLI_CONFIG_PATH:
        print(f"* Error: Config file '{CLI_CONFIG_PATH}' does not exist")
        sys.exit(1)

    if cfg_path:
        try:
            with open(cfg_path, "r") as cf:
                exec(cf.read(), globals())
        except Exception as e:
            print(f"* Error loading config file '{cfg_path}': {e}")
            sys.exit(1)

    if args.debug_mode is not None:
        DEBUG_MODE = args.debug_mode

    if args.env_file:
        DOTENV_FILE = os.path.expanduser(args.env_file)
    else:
        if DOTENV_FILE:
            DOTENV_FILE = os.path.expanduser(DOTENV_FILE)

    if DOTENV_FILE and DOTENV_FILE.lower() == 'none':
        env_path = None
    else:
        try:
            from dotenv import load_dotenv, find_dotenv

            if DOTENV_FILE:
                env_path = DOTENV_FILE
                if not os.path.isfile(env_path):
                    print(f"* Warning: dotenv file '{env_path}' does not exist\n")
                else:
                    load_dotenv(env_path, override=True)
            else:
                env_path = find_dotenv() or None
                if env_path:
                    load_dotenv(env_path, override=True)
        except ImportError:
            env_path = DOTENV_FILE if DOTENV_FILE else None
            if env_path:
                print(f"* Warning: Cannot load dotenv file '{env_path}' because 'python-dotenv' is not installed\n\nTo install it, run:\n    pip install python-dotenv\n\nOnce installed, re-run this tool\n")

    if env_path:
        for secret in SECRET_KEYS:
            val = os.getenv(secret)
            if val is not None:
                globals()[secret] = val

    if args.token_source:
        TOKEN_SOURCE = args.token_source

    if not TOKEN_SOURCE:
        TOKEN_SOURCE = "cookie"

    if TOKEN_SOURCE == "cookie":
        ALARM_TIMEOUT = int((TOKEN_MAX_RETRIES * TOKEN_RETRY_TIMEOUT) + 5)
        try:
            import pyotp
        except ModuleNotFoundError:
            raise SystemExit("Error: Couldn't find the pyotp library !\n\nTo install it, run:\n    pip install pyotp\n\nOnce installed, re-run this tool")

    try:
        from spotipy.oauth2 import SpotifyClientCredentials
    except ModuleNotFoundError:
        raise SystemExit("Error: Couldn't find the spotipy library !\n\nTo install it, run:\n    pip install spotipy\n\nOnce installed, re-run this tool")

    if args.user_agent:
        USER_AGENT = args.user_agent

    if not USER_AGENT:
        if TOKEN_SOURCE == "client":
            USER_AGENT = get_random_spotify_user_agent()
        else:
            USER_AGENT = get_random_user_agent()

    if not check_internet():
        sys.exit(1)

    if args.alt_cookie:
        ALT_COOKIE   = True
        SP_DC_COOKIE = SP_DC_COOKIE2
        LOGIN_REQUEST_BODY_FILE = LOGIN_REQUEST_BODY_FILE2
        GMAIL_TAG    = GMAIL_TAG2
        ERR_CODE     = ERR_CODE2
        SEND_NOTIFY  = SEND_NOTIFY2
        DZ_ALERTS    = DZ_ALERTS2
        ORIG_EMAILS  = ORIG_EMAILS2
        USER_ID      = USER_ID2
        ADD_PLAYLISTS_TO_MONITOR = ADD_PLAYLISTS_TO_MONITOR2
        DEBUG_JMK    = DEBUG_JMK2
        UPDATE_SPREADSHEET = UPDATE_SPREADSHEET2

    if args.jmk:
        JMK_MODE = True
        ALT_VIEW = True

    if args.flag_file:
        FLAG_FILE = os.path.expanduser(args.flag_file)
        flag_file_delete()
    else:
        if FLAG_FILE:
            FLAG_FILE = os.path.expanduser(FLAG_FILE)
            flag_file_delete()

    if args.send_test_email:
        print("* Sending test email notification ...\n")
        if send_email("spotify_monitor: test email", "This is test email - your SMTP settings seems to be correct !", "", SMTP_SSL, smtp_timeout=5) == 0:
            print("* Email sent successfully !")
        else:
            sys.exit(1)
        sys.exit(0)

    if args.check_interval:
        SPOTIFY_CHECK_INTERVAL = args.check_interval
        LIVENESS_CHECK_COUNTER = LIVENESS_CHECK_INTERVAL / SPOTIFY_CHECK_INTERVAL

    if args.offline_timer:
        SPOTIFY_INACTIVITY_CHECK = args.offline_timer

    if args.disappeared_timer:
        SPOTIFY_DISAPPEARED_CHECK_INTERVAL = args.disappeared_timer

    if TOKEN_SOURCE == "client":
        login_request_body_file_param = False
        if args.login_request_body_file:
            LOGIN_REQUEST_BODY_FILE = os.path.expanduser(args.login_request_body_file)
            login_request_body_file_param = True
        else:
            if LOGIN_REQUEST_BODY_FILE:
                LOGIN_REQUEST_BODY_FILE = os.path.expanduser(LOGIN_REQUEST_BODY_FILE)

        if LOGIN_REQUEST_BODY_FILE:
            if os.path.isfile(LOGIN_REQUEST_BODY_FILE):
                try:
                    DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN = parse_login_request_body_file(LOGIN_REQUEST_BODY_FILE)
                except Exception as e:
                    print(f"* Error: Protobuf file ({LOGIN_REQUEST_BODY_FILE}) cannot be processed: {e}")
                    sys.exit(1)
                else:
                    if not args.user_id and not args.list_friends and login_request_body_file_param:
                        print(f"* Login data correctly read from Protobuf file ({LOGIN_REQUEST_BODY_FILE}):")
                        print(" - Device ID:\t\t", DEVICE_ID)
                        print(" - System ID:\t\t", SYSTEM_ID)
                        print(" - User URI ID:\t\t", USER_URI_ID)
                        print(" - Refresh Token:\t", REFRESH_TOKEN, "\n")
                        sys.exit(0)
            else:
                print(f"* Error: Protobuf file ({LOGIN_REQUEST_BODY_FILE}) does not exist")
                sys.exit(1)

        vals = {
            "LOGIN_URL": LOGIN_URL,
            "USER_AGENT": USER_AGENT,
            "DEVICE_ID": DEVICE_ID,
            "SYSTEM_ID": SYSTEM_ID,
            "USER_URI_ID": USER_URI_ID,
            "REFRESH_TOKEN": REFRESH_TOKEN,
        }
        placeholders = {
            "DEVICE_ID": "your_spotify_app_device_id",
            "SYSTEM_ID": "your_spotify_app_system_id",
            "USER_URI_ID": "your_spotify_user_uri_id",
            "REFRESH_TOKEN": "your_spotify_app_refresh_token",
        }

        bad = [
            f"{k} {'missing' if not v else 'is placeholder'}"
            for k, v in vals.items()
            if not v or placeholders.get(k) == v
        ]
        if bad:
            print("* Error:", "; ".join(bad))
            sys.exit(1)

        clienttoken_request_body_file_param = False
        if args.clienttoken_request_body_file:
            CLIENTTOKEN_REQUEST_BODY_FILE = os.path.expanduser(args.clienttoken_request_body_file)
            clienttoken_request_body_file_param = True
        else:
            if CLIENTTOKEN_REQUEST_BODY_FILE:
                CLIENTTOKEN_REQUEST_BODY_FILE = os.path.expanduser(CLIENTTOKEN_REQUEST_BODY_FILE)

        if CLIENTTOKEN_REQUEST_BODY_FILE:
            if os.path.isfile(CLIENTTOKEN_REQUEST_BODY_FILE):
                try:

                    (APP_VERSION, _, _, CPU_ARCH, OS_BUILD, PLATFORM, OS_MAJOR, OS_MINOR, CLIENT_MODEL) = parse_clienttoken_request_body_file(CLIENTTOKEN_REQUEST_BODY_FILE)
                except Exception as e:
                    print(f"* Error: Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}) cannot be processed: {e}")
                    sys.exit(1)
                else:
                    if not args.user_id and not args.list_friends and clienttoken_request_body_file_param:
                        print(f"* Client token data correctly read from Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}):")
                        print(" - App version:\t\t", APP_VERSION)
                        print(" - CPU arch:\t\t", CPU_ARCH)
                        print(" - OS build:\t\t", OS_BUILD)
                        print(" - Platform:\t\t", PLATFORM)
                        print(" - OS major:\t\t", OS_MAJOR)
                        print(" - OS minor:\t\t", OS_MINOR)
                        print(" - Client model:\t", CLIENT_MODEL)
                        sys.exit(0)
            else:
                print(f"* Error: Protobuf file ({CLIENTTOKEN_REQUEST_BODY_FILE}) does not exist")
                sys.exit(1)

        app_version_default = "1.2.62.580.g7e3d9a4f"
        if USER_AGENT and not APP_VERSION:
            try:
                APP_VERSION = ua_to_app_version(USER_AGENT)
            except Exception as e:
                print(f"Warning: wrong USER_AGENT defined, reverting to the default one for APP_VERSION: {e}")
                APP_VERSION = app_version_default
        else:
            APP_VERSION = app_version_default

    else:
        if args.spotify_dc_cookie:
            SP_DC_COOKIE = args.spotify_dc_cookie

        if not SP_DC_COOKIE or SP_DC_COOKIE == "your_sp_dc_cookie_value":
            print("* Error: SP_DC_COOKIE (-u / --spotify_dc_cookie) value is empty or incorrect")
            sys.exit(1)

    if args.oauth_app_creds:
        try:
            SP_APP_CLIENT_ID, SP_APP_CLIENT_SECRET = args.oauth_app_creds.split(":")
        except ValueError:
            print("* Error: -r / --oauth-app-creds has invalid format - use SP_APP_CLIENT_ID:SP_APP_CLIENT_SECRET")
            sys.exit(1)

    if any([
        not SP_APP_CLIENT_ID,
        SP_APP_CLIENT_ID == "your_spotify_app_client_id",
        not SP_APP_CLIENT_SECRET,
        SP_APP_CLIENT_SECRET == "your_spotify_app_client_secret",
    ]):
        print("* Error: SP_APP_CLIENT_ID or SP_APP_CLIENT_SECRET (-r / --oauth-app-creds) value is empty or incorrect")
        sys.exit(1)

    if SP_APP_TOKENS_FILE:
        SP_APP_TOKENS_FILE = os.path.expanduser(SP_APP_TOKENS_FILE)

    if args.list_friends:
        print("* Listing Spotify friends ...\n")
        try:
            if TOKEN_SOURCE == "client":
                sp_accessToken = spotify_get_access_token_from_client_auto(DEVICE_ID, SYSTEM_ID, USER_URI_ID, REFRESH_TOKEN)
            else:
                sp_accessToken = spotify_get_access_token_from_sp_dc(SP_DC_COOKIE)
            sp_friends = spotify_get_friends_json(sp_accessToken)
            spotify_list_friends(sp_friends)
            print("─" * HORIZONTAL_LINE)
        except Exception as e:
            print(f"* Error: {e}")
            sys.exit(1)
        sys.exit(0)

    if not args.user_id:
        print("* Error: SPOTIFY_USER_URI_ID argument is required !")
        sys.exit(1)

    if args.monitor_list:
        MONITOR_LIST_FILE = os.path.expanduser(args.monitor_list)
    else:
        if MONITOR_LIST_FILE:
            MONITOR_LIST_FILE = os.path.expanduser(MONITOR_LIST_FILE)

    if MONITOR_LIST_FILE:
        try:
            try:
                with open(MONITOR_LIST_FILE, encoding="utf-8") as file:
                    lines = file.read().splitlines()
            except UnicodeDecodeError:
                with open(MONITOR_LIST_FILE, encoding="cp1252") as file:
                    lines = file.read().splitlines()

            sp_tracks = [
                line.strip()
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]
        except Exception as e:
            print(f"* Error: File with monitored Spotify tracks cannot be opened: {e}")
            sys.exit(1)
    else:
        sp_tracks = []

    if args.csv_file:
        CSV_FILE = os.path.expanduser(args.csv_file)
    else:
        if CSV_FILE:
            CSV_FILE = os.path.expanduser(CSV_FILE)

    if CSV_FILE:
        try:
            with open(CSV_FILE, 'a', newline='', buffering=1, encoding="utf-8") as _:
                pass
        except Exception as e:
            print(f"* Error: CSV file cannot be opened for writing: {e}")
            sys.exit(1)

    if args.file_suffix:
        FILE_SUFFIX = str(args.file_suffix)
    else:
        if not FILE_SUFFIX:
            FILE_SUFFIX = str(args.user_id)

    if args.truncate:
        if args.truncate != 999:
            TRUNCATE_CHARS = args.truncate
        else:
            try:
                terminal_size = shutil.get_terminal_size()
                if ALT_VIEW:
                    print_to_screen(f"The detected terminal screen width is: {terminal_size.columns} characters\n")
                    print_to_screen(f"")
                else:
                    print(f"The detected terminal screen width is: {terminal_size.columns} characters\n")
                TRUNCATE_CHARS = terminal_size.columns
            except Exception as e:
                if ALT_VIEW:
                    print_to_screen(f"Error: Cannot determine terminal screen width: {e}")
                    print_to_screen(f"")
                else:
                    print(f"Error: Cannot determine terminal screen width: {e}")
                sys.exit(1)

    if args.disable_logging is True:
        DISABLE_LOGGING = True

    if not DISABLE_LOGGING:
        log_path = Path(os.path.expanduser(SP_LOGFILE))
        if log_path.parent != Path('.'):
            if log_path.suffix == "":
                log_path = log_path.parent / f"{log_path.name}_{FILE_SUFFIX}.log"
        else:
            if log_path.suffix == "":
                log_path = Path(f"{log_path.name}_{FILE_SUFFIX}.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        FINAL_LOG_PATH = str(log_path)
        sys.stdout = Logger(FINAL_LOG_PATH, mode="both")
    else:
        FINAL_LOG_PATH = None

    # Create persistent Logger instances
    if not DISABLE_LOGGING:
        log_logger = Logger(FINAL_LOG_PATH, mode="log")
        #screen_logger = Logger(FINAL_LOG_PATH, mode="screen")
        #both_logger = Logger(FINAL_LOG_PATH, mode="both")

    
    if args.notify_active is True:
        ACTIVE_NOTIFICATION = True

    if args.notify_inactive is True:
        INACTIVE_NOTIFICATION = True

    if args.notify_track is True:
        TRACK_NOTIFICATION = True

    if args.notify_song_changes is True:
        SONG_NOTIFICATION = True

    if args.notify_loop is True:
        SONG_ON_LOOP_NOTIFICATION = True

    if args.notify_errors is False:
        ERROR_NOTIFICATION = False

    if args.track_in_spotify is True:
        TRACK_SONGS = True

    if SMTP_HOST.startswith("your_smtp_server_"):
        ACTIVE_NOTIFICATION = False
        INACTIVE_NOTIFICATION = False
        TRACK_NOTIFICATION = False
        SONG_NOTIFICATION = False
        SONG_ON_LOOP_NOTIFICATION = False
        ERROR_NOTIFICATION = False

    print(f"* Spotify polling intervals:\t[check: {display_time(SPOTIFY_CHECK_INTERVAL)}] [inactivity: {display_time(SPOTIFY_INACTIVITY_CHECK)}]\n*\t\t\t\t[disappeared: {display_time(SPOTIFY_DISAPPEARED_CHECK_INTERVAL)}] [error: {display_time(SPOTIFY_ERROR_INTERVAL)}]")
    print(f"* Email notifications:\t\t[active = {ACTIVE_NOTIFICATION}] [inactive = {INACTIVE_NOTIFICATION}] [tracked = {TRACK_NOTIFICATION}]\n*\t\t\t\t[songs on loop = {SONG_ON_LOOP_NOTIFICATION}] [every song = {SONG_NOTIFICATION}] [errors = {ERROR_NOTIFICATION}]")
    print(f"* Token source:\t\t\t{TOKEN_SOURCE} + oauth_app")
    print(f"* Track listened songs:\t\t{TRACK_SONGS}")
    # print(f"* User agent:\t\t\t{USER_AGENT}")
    print(f"* Liveness check:\t\t{bool(LIVENESS_CHECK_INTERVAL)}" + (f" ({display_time(LIVENESS_CHECK_INTERVAL)})" if LIVENESS_CHECK_INTERVAL else ""))
    print(f"* CSV logging enabled:\t\t{bool(CSV_FILE)}" + (f" ({CSV_FILE})" if CSV_FILE else ""))
    print(f"* Alert on monitored tracks:\t{bool(MONITOR_LIST_FILE)}" + (f" ({MONITOR_LIST_FILE})" if MONITOR_LIST_FILE else ""))
    print(f"* Output logging enabled:\t{not DISABLE_LOGGING}" + (f" ({FINAL_LOG_PATH})" if not DISABLE_LOGGING else ""))
    print(f"* Debug mode:\t\t\t{DEBUG_MODE}")
    if not DISABLE_LOGGING and TRUNCATE_CHARS > 0:
        print(f"* Truncate terminal lines:\t{TRUNCATE_CHARS} chars")
    print(f"* Spotify OAuth cache file:\t{SP_APP_TOKENS_FILE if SP_APP_TOKENS_FILE else 'None (memory only)'}")
    if FLAG_FILE:
        print(f"* Flag file:\t\t\t{FLAG_FILE}")
    print(f"* Configuration file:\t\t{cfg_path}")
    print(f"* Dotenv file:\t\t\t{env_path or 'None'}\n")
    print(f"* Visual Mode:\t\t\t" + (f"Alternate" if JMK_MODE else "Standard") + (f" (with DEBUG_JMK level {DEBUG_JMK})" if JMK_MODE else ""))
    print(f"* Send original emails:\t\t{ORIG_EMAILS}")
    print(f"* Send NTFY notifications:\t{SEND_NOTIFY}")
    print(f"* Discovery Zone Alerts:\t{DZ_ALERTS}")
    print(f"* Spreadsheet updates:\t\t{UPDATE_SPREADSHEET}" + (f" (tab: {ERR_CODE})" if UPDATE_SPREADSHEET else ""))
    print("")

    # We define signal handlers only for Linux, Unix & MacOS since Windows has limited number of signals supported
    if platform.system() != 'Windows':
        signal.signal(signal.SIGUSR1, toggle_active_inactive_notifications_signal_handler)
        signal.signal(signal.SIGUSR2, toggle_song_notifications_signal_handler)
        signal.signal(signal.SIGCONT, toggle_track_notifications_signal_handler)
        signal.signal(signal.SIGPIPE, toggle_songs_on_loop_notifications_signal_handler)
        signal.signal(signal.SIGTRAP, increase_inactivity_check_signal_handler)
        signal.signal(signal.SIGABRT, decrease_inactivity_check_signal_handler)
        signal.signal(signal.SIGHUP, reload_secrets_signal_handler)

    for playlist in ADD_PLAYLISTS_TO_MONITOR:
        periodic_load_tracks_flexible(playlist)

    if INITIAL_STARTUP:
        INITIAL_STARTUP = False
        print("")

    spotify_monitor_friend_uri(args.user_id, sp_tracks, CSV_FILE)

    sys.stdout = stdout_bck
    sys.exit(0)


if __name__ == "__main__":
    main()