import sqlite3


def start_database_init(app_logs, MAX_LOG_ENTRIES, log_manager):
    log_message = "Initializing databases..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    song_conn = sqlite3.connect("auto_content_generator/midnight_smokey/databases/song_database.db")
    song_cursor = song_conn.cursor()

    song_cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        song TEXT,
        song_name TEXT,
        artist_name TEXT,
        song_id TEXT PRIMARY KEY,
        duration TEXT,
        development_status TEXT
    );
    """)

    song_conn.commit()
    song_conn.close()

    article_conn = sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db")
    article_cursor = article_conn.cursor()

    article_cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        title TEXT,
        image_url TEXT,
        article_url TEXT,
        contents TEXT,
        category TEXT,
        instagram_contents TEXT,
        twitter_contents TEXT,
        facebook_contents TEXT,
        development_status TEXT
    );
    """)

    article_conn.commit()
    article_conn.close()