import sqlite3
import os

def is_duplicate(article_url):
    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE article_url = ?", (article_url,))
        data = c.fetchone()
        return bool(data)

def add_article(title, image_url, article_url, development_status="unprocessed"):
    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO articles (title, image_url, article_url, development_status) VALUES (?, ?, ?, ?)",
                    (title, image_url, article_url, development_status))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Duplicate article URL found: {article_url}")


def validate_and_delete_incomplete_articles(log_manager, app_logs, MAX_LOG_ENTRIES):
    print("Validating preprocessed articles")

    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM articles WHERE development_status = 'preprocessed'")
        rows = c.fetchall()

        for row in rows:
            title, image_url, article_url = row[:3]
            development_status = row[-1]
            contents = row[3]

            if not all([title, image_url, article_url, development_status, contents]):
                print(f"Deleting incomplete record for article with URL: {article_url}")
                log_message = f"Deleting incomplete article for {article_url}"
                if len(app_logs) >= MAX_LOG_ENTRIES:
                    app_logs.pop(0)
                log_manager.append_log(log_message)

                c.execute("DELETE FROM articles WHERE article_url = ?", (article_url,))
            elif not image_url.lower().endswith(('.jpg', '.jpeg')):
                print(f"Deleting record with invalid image URL for article with URL: {article_url}")
                log_message = f"Deleting article with invalid image URL for {article_url}"
                if len(app_logs) >= MAX_LOG_ENTRIES:
                    app_logs.pop(0)
                log_manager.append_log(log_message)

                try:
                    os.remove(image_url)
                    print(f"Successfully deleted file: {image_url}")
                    log_message = f"Successfully deleted image: {image_url}"
                    if len(app_logs) >= MAX_LOG_ENTRIES:
                        app_logs.pop(0)
                    log_manager.append_log(log_message)

                except Exception as e:
                    print(f"Failed to delete file: {image_url}. Reason: {str(e)}")
                    log_message = f"Failed to delete image: {image_url}. Reason {str(e)}"
                    if len(app_logs) >= MAX_LOG_ENTRIES:
                        app_logs.pop(0)
                    log_manager.append_log(log_message)

                c.execute("DELETE FROM articles WHERE article_url = ?", (article_url,))

        conn.commit()
        print("Validating complete")



def load_random_preprocessed_article():
    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM articles WHERE development_status = 'preprocessed' ORDER BY RANDOM() LIMIT 1;")

        random_article = c.fetchone()

        if random_article is not None:
            title, image_url, article_url, contents, category, instagram_contents, twitter_contents, facebook_contents, development_status = random_article
            print("Random article details:")
            print(f"Title: {title}")
            print(f"Image URL: {image_url}")
            print(f"Article URL: {article_url}")
            print(f"Contents: {contents}")
            print(f"Category: {category}")
            print(f"Instagram Contents: {instagram_contents}")
            print(f"Twitter Contents: {twitter_contents}")
            print(f"Facebook Contents: {facebook_contents}")
            print(f"Development Status: {development_status}")
            return random_article
        else:
            return None


def delete_article_by_url(article_url):
    try:
        conn = sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db")
        c = conn.cursor()

        c.execute("DELETE FROM articles WHERE article_url = ?", (article_url,))

        conn.commit()

        conn.close()

        print(f"Article with URL {article_url} has been deleted.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def update_development_status_to_uploaded(article_url):

    with sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db") as conn:
        c = conn.cursor()
        try:
            c.execute("UPDATE articles SET development_status = 'uploaded' WHERE article_url = ?", (article_url,))

            conn.commit()

            if c.rowcount:
                print(f"Updated development_status to 'uploaded' for article with URL: {article_url}")
            else:
                print(f"No article found with URL: {article_url}")

        except sqlite3.Error as e:
            print(f"An error occurred while updating: {e}")

def delete_article_by_image_url(image_url):
    try:
        conn = sqlite3.connect("auto_content_generator/mock_times/databases/article_database.db")
        c = conn.cursor()

        c.execute("DELETE FROM articles WHERE image_url = ?", (image_url,))

        conn.commit()

        if c.rowcount:
            print(f"Article with image URL {image_url} has been deleted.")
        else:
            print(f"No article found with image URL: {image_url}")

        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
