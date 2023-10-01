import requests
import json
import random

api_key = ""
collection_id = ""


def start_webflow_upload(updated_article3, uploaded_image_main, uploaded_image_thumbnail, app_logs, MAX_LOG_ENTRIES, log_manager):
    title = updated_article3[0]
    contents = updated_article3[3]
    category = updated_article3[4]

    possible_authors = ["", "", "",
                        "", "", ""]
    author = random.choice(possible_authors)

    time = random.randint(5, 11)
    print(time)

    category_to_id = {
        'World': '',
        'US': '',
        'Science': '',
        'Health': '',
        'Finance': '',
        'Entertainment': '',
        'Politics': '',
        'Sports': '',
        'Miscellaneous': ''
    }
    category = category_to_id.get(category, "Unknown")

    endpoint_url = f"https://api.webflow.com/collections/{collection_id}/items"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept-version": "1.0.0",
        "Content-Type": "application/json"
    }

    fields = {
        "name": title,
        "category": category,
        "author": author,
        "time": time,
        "thumb-image": uploaded_image_thumbnail,
        "main-image": uploaded_image_main,
        "news-details": contents,
        "_archived": False,
        "_draft": False
    }

    response = requests.post(endpoint_url, headers=headers, data=json.dumps({"fields": fields}))
    print(response)

    url = "https://api.webflow.com/sites//publish"
    payload = {"domains": ["www.mocktimes.com"]}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept-version": "1.0.0",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        log_message = "Article Successfully Uploaded to Mock Times Website!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
    else:
        log_message = "There was a problem uploading to website..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
    return
