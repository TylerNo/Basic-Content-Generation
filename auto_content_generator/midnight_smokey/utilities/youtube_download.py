import yt_dlp
import os

def start_youtube_download(random_song):
    print("Youtube Downloader Starting...")
    song = random_song[0]
    duration = random_song[4]
    song_length = int(duration) // 1000

    search_term = song

    ydl_opts = {
        'default_search': f'ytsearch5:{search_term}',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'auto_content_generator/midnight_smokey/assets/temp/audio',
        'quiet': True,
        'no_warnings': True,
        'fragment-retries': 'infinite',
        'retries': 20,
        'retry-sleep': 'linear=1::5',
        'buffer-size': '16K',
        'http-chunk-size': '1M',
        'limit-rate': '25K',
        'source_address': '0.0.0.0',
        'user-agent': '',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(search_term, download=False)
            matching_entries = [
                entry for entry in result['entries']
                if abs(entry['duration'] - song_length) <= 3
            ]

            if matching_entries:
                video_url = matching_entries[0]['url']
                ydl.download([video_url])
                print(f"Downloaded Song Successfully!")
                dl_flag_success = True
                return dl_flag_success
            else:
                print(f"No matching video found for {song} within 3 seconds difference.")
                dl_flag_success = False
                return dl_flag_success
        except Exception as e:
            print(f"Error: {e}")
            print(f"Could not download {song}.")
            dl_flag_success = False
            return dl_flag_success
