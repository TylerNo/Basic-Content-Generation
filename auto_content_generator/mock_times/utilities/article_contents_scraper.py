import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import secrets
from auto_content_generator.mock_times.databases.mt_database_manager import delete_article_by_image_url, delete_article_by_url

ASSETS_PATH = "auto_content_generator/mock_times/assets/pictures"


def generate_random_string(length=20):
    return secrets.token_hex(length // 2)


def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        file_extension = os.path.splitext(image_url)[1]

        if not file_extension:
            content_type = response.headers.get('content-type')

            if "image/jpeg" in content_type or "image/jpg" in content_type:
                file_extension = ".jpg"
            elif "image/png" in content_type:
                file_extension = ".png"
            elif "image/gif" in content_type:
                file_extension = ".gif"
            else:
                file_extension = ".jpg"

        random_filename = generate_random_string() + file_extension
        filepath = os.path.join(ASSETS_PATH, random_filename)

        with open(filepath, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8192):
                fd.write(chunk)

        return filepath
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
        delete_article_by_image_url(image_url)
        return None


def get_main_image_url(soup, article_url, app_logs, MAX_LOG_ENTRIES, log_manager):

    search_classes = ["caas-img-wrapper", "caas-carousel-figure", "caas-img-container"]

    for class_name in search_classes:
        container = soup.find('div', class_=class_name)
        if container:
            img = container.find('img', src=True)
            if img:
                return img['src']

    print("Can't find image, deleting article with URL " + article_url)
    log_message = "Can't find image, deleting article: " + article_url
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    delete_article_by_url(article_url)
    return None




def scrape_article_content(article_url, app_logs, MAX_LOG_ENTRIES, log_manager):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    content = ' '.join(p.text for p in paragraphs)

    main_image_url = get_main_image_url(soup, article_url, app_logs, MAX_LOG_ENTRIES, log_manager)

    return content, main_image_url


def preprocess_articles(app_logs, MAX_LOG_ENTRIES, log_manager):
    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE development_status = 'unprocessed'")
        rows = c.fetchall()
        for row in rows:
            title, _, article_url, *_ = row

            print("Starting preprocess for " + article_url)
            log_message = "Starting Content Scraper for Article: " + article_url
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            content, main_image_url = scrape_article_content(article_url, app_logs, MAX_LOG_ENTRIES, log_manager)

            local_path = download_image(main_image_url) if main_image_url else None

            if local_path:
                c.execute("UPDATE articles SET image_url=?, development_status='preprocessed' WHERE article_url=?",
                          (local_path, article_url))

                c.execute("UPDATE articles SET contents=? WHERE article_url=?", (content, article_url))

                conn.commit()
        print("Preprocessing complete")
        log_message = "Article Content Scraper Completed!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)