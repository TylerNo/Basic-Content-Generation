import sqlite3


def update_song_database(song_name, artist_name, duration, song_id, development_status, app_logs, MAX_LOG_ENTRIES, log_manager):
    conn = sqlite3.connect("auto_content_generator/midnight_smokey/databases/song_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM songs WHERE song_id=?", (song_id,))
    if cursor.fetchone():
        log_message = song_name + " Already Exists in Database!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        return

    song = f"{artist_name} - {song_name}"

    try:
        cursor.execute(
            "INSERT INTO songs (song, song_name, artist_name, song_id, duration, development_status) VALUES (?, ?, ?, ?, ?, ?)",
            (song, song_name, artist_name, song_id, duration, development_status))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def get_random_scraped_song():
    conn = sqlite3.connect("auto_content_generator/midnight_smokey/databases/song_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM songs WHERE development_status='scraped' ORDER BY RANDOM() LIMIT 1;")
        random_song = cursor.fetchone()

        if random_song is not None:
            song, song_name, artist_name, song_id, duration, development_status = random_song
            print(f"Random scraped song: {artist_name} - {song_name}")
            return random_song
        else:
            print("No scraped songs found in the database.")
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()


def update_development_status_to_uploaded(song_id, app_logs, MAX_LOG_ENTRIES, log_manager):
    conn = sqlite3.connect("auto_content_generator/midnight_smokey/databases/song_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE songs SET development_status='uploaded' WHERE song_id=?", (song_id,))
        if cursor.rowcount == 0:
            print(f"No song found with song ID {song_id} to update.")
        else:
            print(f"Successfully updated development_status to 'uploaded' for song ID {song_id}")
            log_message = "Updated Development Status to 'Uploaded'!"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()