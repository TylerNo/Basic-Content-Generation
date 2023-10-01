import requests
from bs4 import BeautifulSoup
from auto_content_generator.mock_times.databases.mt_database_manager import is_duplicate, add_article


def save_to_db(title, image_url, article_url, app_logs, MAX_LOG_ENTRIES, log_manager):
    if not title or not image_url or not article_url:
        print(f"Skipping article due to missing data.")
        log_message = "Skipping Article due to missing data."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return

    if not is_duplicate(article_url):
        add_article(title, image_url, article_url)
        print(f"Article '{title}' saved to database!")
        log_message = "Article saved to database!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
    else:
        print(f"Article '{title}' is a duplicate and was not saved.")
        log_message = "Article is a duplicate and was not saved."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)


def get_full_url(base, relative):
    if relative.startswith("/"):
        relative = relative[1:]
    return f"{base}{relative}"


def extract_data_from_items(items, base_url, app_logs, MAX_LOG_ENTRIES, log_manager):
    for item in items:
        try:
            relative_link = item.find('a')['href']
            link = get_full_url(base_url, relative_link)

            title = item.find('h3', class_='LineClamp(2,2.6em) Mend(50px) Mb(4px) Lh(1.33) Fz(18px) Fz(16px)--maw1024 Fw(b) stream-item-title').text.strip()

            image_1 = item.find('img')['src']

            print("Title:", title)
            print("Image URL:", image_1)
            print("Article URL:", link)
            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)


        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)

def start_article_scraper(app_logs, MAX_LOG_ENTRIES, log_manager):
    print("Article scraper starting...")

    print('-' * 50)
    print("Starting scraping on news.yahoo.com")
    print('-' * 50)

    log_message = "Starting Scraper on 'news.yahoo.com'..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    URL = "https://news.yahoo.com/"
    headers = {
        "User-Agent": ""
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_article = soup.find("div", class_="ntk-lead ntk-link-filter ntk-wrap D(f) Pos(r)")
    if main_article:
        try:
            title = main_article.find("h2", id="ntk-title").text.strip()
            print("Title:", title)
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            image_1 = main_article.find("img")["src"]
            print("Image URL:", image_1)
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            link = main_article.find("a", {"data-test-locator": "lead-content-link"})["href"]
            full_link = get_full_url("https://news.yahoo.com/", link)  # Convert to full link
            link = full_link
            print("Article URL:", link)
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)


        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    sub_main_articles = soup.find_all("li", class_="ntk-item W(1/5) List(n) ntk-wrap H(100%)")

    for article in sub_main_articles:
        try:
            title = article.select_one('h3').text
            image_element = article.select_one('img.StretchedBox')
            image_1 = image_element['src'] if image_element else None
            link_element = article.select_one('a[data-test-locator="item-link"]')
            link = link_element['href'] if link_element else None
            full_link = get_full_url("https://news.yahoo.com/", link)  # Convert to full link
            link = full_link

            print("Title:", title)
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Image URL:", image_1)
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Article URL:", link)
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)


        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    items = soup.find_all('li', class_='stream-item js-stream-content Bgc(t) Pos(r) Mb(24px)')
    extract_data_from_items(items, "https://news.yahoo.com/", app_logs, MAX_LOG_ENTRIES, log_manager)

    for category in ["politics", "health", "science"]:
        print(f"Starting scraping on news.yahoo.com/{category}")
        log_message = f"Starting Scraper on 'news.yahoo.com/{category}"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        URL = f"https://news.yahoo.com/{category}/"
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('li', class_='stream-item js-stream-content Bgc(t) Pos(r) Mb(24px)')
        extract_data_from_items(items, URL, app_logs, MAX_LOG_ENTRIES, log_manager)


    print("Starting scraping on yahoo.com/entertainment")
    log_message = "Starting Scraper on 'yahoo.com/entertainment'"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    URL = "https://www.yahoo.com/entertainment/"
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        link = soup.find('a', {'data-test-locator': 'lead-content-link'}).get('href')
        full_link = get_full_url("https://www.yahoo.com/entertainment/", link)  # Convert to full link
        link = full_link

        image_1 = soup.find('img', {'data-test-locator': 'lead-item-image'}).get('src')

        title = soup.find('h2', {'id': 'ntk-title'}).text.strip()
        print("Title:", title)
        log_message = "Title: " + title
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print("Image URL:", image_1)
        log_message = "Image URL: " + image_1
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print("Article URL:", link)
        log_message = "Article URL: " + link
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)

    except (AttributeError, TypeError) as e:
        print(f"Error encountered: {e}")
        pass

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    sub_main_articles = soup.find_all('li', class_='ntk-item W(1/5) List(n) ntk-wrap H(100%)')

    for article in sub_main_articles:
        try:
            link = article.find('a', {'data-test-locator': 'item-link'}).get('href')
            full_link = get_full_url("https://www.yahoo.com/entertainment/", link)  # Convert to full link
            link = full_link

            image_1 = article.find('img', {'data-test-locator': 'item-image'}).get('src')

            title = article.find('h3', {'data-test-locator': 'item-title'}).text.strip()

            print("Title:", title)
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Image URL:", image_1)
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Article URL:", link)
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)


        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    stream_articles = soup.find_all('li', class_='stream-item js-stream-content Bgc(t) Pos(r) Mb(24px)')

    for article in stream_articles:
        try:
            link = article.find('a', {'data-test-locator': 'stream-item-image'}).get('href')
            full_link = get_full_url("https://www.yahoo.com/entertainment/", link)  # Convert to full link
            link = full_link

            image_1 = article.find('img', {'data-test-locator': 'stream-item-image'}).get('src')

            title = article.find('h3', {'data-test-locator': 'stream-item-title'}).find('a').text.strip()

            print("Title:", title)
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Image URL:", image_1)
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print("Article URL:", link)
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)


        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    print("Starting scraping on finance.yahoo.com")
    log_message = "Starting Scraper on 'finance.yahoo.com'"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    URL = "https://finance.yahoo.com/"
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        link = soup.find('a', {'class': 'js-content-viewer'}).get('href')
        full_link = get_full_url("https://finance.yahoo.com/", link)
        link = full_link

        image_1 = soup.find('img', {'alt': True}).get('src')

        title = soup.find('h2').text.strip()

        print("Title:", title)
        log_message = "Title: " + title
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print("Image URL:", image_1)
        log_message = "Image URL: " + image_1
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print("Article URL:", link)
        log_message = "Article URL: " + link
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)
    except (AttributeError, TypeError) as e:
        print(f"Error encountered: {e}")
        pass

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    items = soup.find_all('li', class_='Pos(r) dustyImage D(b) Whs(n) Mb(6%) Mb(5.4%)--md1100')

    for item in items:
        try:
            link = item.a['href']
            full_link = get_full_url("https://finance.yahoo.com/", link)
            link = full_link


            title = item.h3.text

            image_1 = item.img['src']

            print(f"Title: {title}")
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Image Link: {image_1}")
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Href Link: {link}")
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)
        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    items = soup.find_all('li', class_='js-stream-content Pos(r)')

    for item in items:
        try:
            link = item.a['href']
            full_link = get_full_url("https://finance.yahoo.com/", link)  # Convert to full link
            link = full_link


            title = item.h3.text.strip()

            image_1 = item.img['src']

            print(f"Title: {title}")
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Image Link: {image_1}")
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Href Link: {link}")
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)

        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    print("Starting scraping on sports.yahoo.com")
    log_message = "Starting Scraper on 'sports.yahoo.com'"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    URL = "https://sports.yahoo.com/"
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        item = soup.find('div', class_='_ys_13mq8u1')

        link = item.a['href']

        title = item.h3.text.strip()

        image_1 = item.img['src']

        print(f"Title: {title}")
        log_message = "Title: " + title
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print(f"Image Link: {image_1}")
        log_message = "Image URL: " + image_1
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        print(f"Href Link: {link}")
        log_message = "Article URL: " + link
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)

    except (AttributeError, TypeError) as e:
        print(f"Error encountered: {e}")
        pass

    print('-' * 50)
    log_message = "-" * 50
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    items = soup.find_all('div', class_='_ys_hudz05')

    for item in items:
        try:
            link = item.a['href']

            title = item.h3.text.strip()

            image_1 = item.img['src']

            print(f"Title: {title}")
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Image Link: {image_1}")
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Href Link: {link}")
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)

        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    list_items = soup.find_all('li', class_='js-stream-content Pos(r) YahooSans Fw(400)!')

    for item in list_items:
        try:
            title_element = item.find('a', class_='mega-item-header-link')
            title = title_element.text.strip() if title_element else None

            img_element = item.find('img')
            image_1 = img_element['src'] if img_element else None

            link = title_element['href'] if title_element else None

            print(f"Title: {title}")
            log_message = "Title: " + title
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Image Link: {image_1}")
            log_message = "Image URL: " + image_1
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            print(f"Href Link: {link}")
            log_message = "Article URL: " + link
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            save_to_db(title, image_1, link, app_logs, MAX_LOG_ENTRIES, log_manager)

        except (AttributeError, TypeError) as e:
            print(f"Error encountered: {e}")
            pass

        print('-' * 50)
        log_message = "-" * 50
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
