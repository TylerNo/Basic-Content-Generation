import json
import requests
import time


def start_twitter_upload(uploaded_image_thumbnail, twitter_contents, app_logs, MAX_LOG_ENTRIES, log_manager):
    print("Twitter upload starting...")
    url = "https://app.publer.io/api/v1/media/from-url"

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": "",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": "",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "",
    }

    data = {
        "media": [{"url": uploaded_image_thumbnail}],
        "type": "single",
        "directUpload": False,
        "inLibrary": False,
        "token": None,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful!")

        try:
            response_data = response.json()
            job_id = response_data.get("job_id")

            if job_id:
                print(f"Job ID: {job_id}")
            else:
                print("Job ID not found in the response.")

        except json.JSONDecodeError:
            print("Failed to parse JSON response.")

    else:
        print(f"Failed to make the request. Status code: {response.status_code}")
        print(response.text)


    url = f"https://app.publer.io/api/v1/job_status/{job_id}"

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": "",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "",
    }

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                response_data = response.json()
                print(json.dumps(response_data, indent=4))

                status = response_data.get("status")
                if status == "complete":
                    print("Image upload complete.")
                    path = response_data['payload'][0]['path']
                    thumb_path = response_data['payload'][0]['thumbnail']
                    payload_id = response_data['payload'][0]['id']
                    break


            except json.JSONDecodeError:
                print("Failed to parse JSON response.")

        else:
            print(f"Failed to make the request. Status code: {response.status_code}")
            print(response.text)

        time.sleep(2)

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": "",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ""
    }

    data = {
        "bulk": {
            "state": "scheduled",
            "url": "publish",
            "posts": [
                {
                    "id": "post_0",
                    "networks": {
                        "default": {
                            "type": "photo",
                            "text": str(twitter_contents) + " #News",
                            "media": [
                                {
                                    "id": payload_id,
                                    "name": "",
                                    "type": "photo",
                                    "path": path,
                                    "thumbnail": thumb_path,
                                    "validity": {
                                        "twitter": True,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": True,
                                        "facebook": {
                                            "post": True,
                                            "reel": False
                                        },
                                        "instagram": {
                                            "post": True,
                                            "story": True,
                                            "reel": False
                                        },
                                        "youtube": {
                                            "video": False,
                                            "short": False
                                        },
                                        "tiktok": False,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1296,
                                    "height": 630,
                                    "caption": ""
                                }
                            ]
                        },
                        "twitter": {
                            "type": "photo",
                            "text": twitter_contents + " #News",
                            "media": [
                                {
                                    "id": payload_id,
                                    "name": "",
                                    "type": "photo",
                                    "path": path,
                                    "thumbnail": thumb_path,
                                    "validity": {
                                        "twitter": True,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": True,
                                        "facebook": {
                                            "post": True,
                                            "reel": False
                                        },
                                        "instagram": {
                                            "post": True,
                                            "story": True,
                                            "reel": False
                                        },
                                        "youtube": {
                                            "video": False,
                                            "short": False
                                        },
                                        "tiktok": False,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1296,
                                    "height": 630,
                                    "caption": ""
                                }
                            ]
                        }
                    },
                    "accounts": [
                        {
                            "id": "64eb3cd3db2797268280d928",
                            "previewed_link": False,
                            "previewed_media": False,
                            "labels": []
                        }
                    ],
                    "labels": []
                }
            ]
        }
    }

    url = "https://app.publer.io/api/v1/posts/schedule/publish"

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Request was successful!")
        log_message = "Article Successfully Uploaded to Mock Times Twitter!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        try:
            response_data = response.json()
            print(json.dumps(response_data, indent=4))
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
            log_message = "There was a problem uploading to Twitter..."
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)
    else:
        print(f"Failed to make the request. Status code: {response.status_code}")
        log_message = "There was a problem uploading to Twitter..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        print(response.text)


