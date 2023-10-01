import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from auto_content_generator.midnight_smokey.databases.ms_database_manager import update_song_database


def start_song_scraper(app_logs, MAX_LOG_ENTRIES, config, log_manager):
    log_message = "Song Scraper Starting..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    playlists = config['spotify']['playlists']
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']
    development_status = "scraped"

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    for playlist in playlists:
        offset = 0

        while True:
            results = sp.playlist_tracks(playlist, offset=offset)
            if len(results['items']) == 0:
                break

            for idx, item in enumerate(results['items']):
                track = item['track']

                try:
                    song_name = track['name']
                    artist_name = track['artists'][0]['name']
                    song_id = track['id']
                    duration = track['duration_ms']

                    log_message = song_name + " by " + artist_name + " successfully scraped!"
                    if len(app_logs) >= MAX_LOG_ENTRIES:
                        app_logs.pop(0)
                    log_manager.append_log(log_message)

                    update_song_database(song_name, artist_name, duration, song_id, development_status, app_logs,
                                         MAX_LOG_ENTRIES, log_manager)

                except TypeError:
                    error_message = "Error processing song in playlist {}. Skipping to the next song.".format(playlist)
                    if len(app_logs) >= MAX_LOG_ENTRIES:
                        app_logs.pop(0)
                    log_manager.append_log(error_message)
                    continue

            offset += len(results['items'])



