from auto_content_generator.midnight_smokey.utilities.song_scraper import start_song_scraper
from auto_content_generator.mock_times.utilities.article_scraper import start_article_scraper
from auto_content_generator.mock_times.utilities.article_contents_scraper import preprocess_articles

def start_scraper_manager(app_logs, MAX_LOG_ENTRIES, config, log_manager):
    log_message = "Scraper Manager Starting..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Starting Song Scraper..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)
    start_song_scraper(app_logs, MAX_LOG_ENTRIES, config, log_manager)

    log_message = "Starting Article Scraper..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)
    start_article_scraper(app_logs, MAX_LOG_ENTRIES, log_manager)

    log_message = "Starting Article Contents Scraper..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)
    preprocess_articles(app_logs, MAX_LOG_ENTRIES, log_manager)

    return
