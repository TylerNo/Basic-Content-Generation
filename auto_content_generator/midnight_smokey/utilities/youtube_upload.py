import requests
import time
from datetime import datetime, timedelta
import random


def start_youtube_upload(uploaded_file, random_song):
    print("Starting Youtube Upload via Publer")

    options = ["", "", ""]
    youtube_account = random.choice(options)

    song_name = random_song[1]
    artist_name = random_song[2]
    video_title = (song_name + " - " + artist_name + " (Slowed & Reverb)")
    video_desc = 'be sure to like and subscribe for more slowed and reverb videos :)'
    link = uploaded_file

    current_time = datetime.now()

    base_scheduled_time = current_time + timedelta(hours=5)

    # Format the time
    schedule_date = base_scheduled_time.strftime('%Y-%m-%dT%H:%M') + "-07:00"
    print(schedule_date)

    url = "https://app.publer.io/api/v1/media/from-url"

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": '',
        "origin": "https://app.publer.io",
        "publer-workspace-id": "",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ""
    }

    data = {
        "media": [{"url": link}],
        "type": "single",
        "directUpload": False,
        "inLibrary": False,
        "token": None
    }

    response = requests.post(url, headers=headers, json=data)
    print(response)


    json_response = response.json()
    print(json_response)
    text_value = json_response.get("job_id", None)
    print(text_value)



    url = "https://app.publer.io/api/v1/job_status/" + text_value

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": '',
        "publer-workspace-id": "64e020d9db279792c3f546f7",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ""
    }

    while True:
        response = requests.get(url, headers=headers)
        print(response)
        response_data = response.json()
        print(response_data)

        payload = response_data.get('payload')
        if payload and isinstance(payload, list) and payload[0].get('error') == 'Timed out while reading data':
            return None

        if response_data.get('status') == 'complete':
            break

        time.sleep(2)






    media_payload = response_data['payload'][0]
    media_id = media_payload['id']
    media_name = media_payload['name']
    media_type = media_payload['type']
    media_path = media_payload['path']
    media_validity = media_payload['validity']
    media_width = media_payload['width']
    media_height = media_payload['height']
    media_thumbnails = media_payload['thumbnails']


    url = "https://app.publer.io/api/v1/posts/schedule"

    headers = {
        "authority": "app.publer.io",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": "",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "",
    }

    cookies = {

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
                            "type": "video",
                            "details": {},
                            "title": video_title,
                            "text": video_desc,
                            "media": [
                                {
                                    "id": media_id,
                                    "name": None,
                                    "type": "video",
                                    "path": media_path,
                                    "validity": {
                                        "twitter": False,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": False,
                                        "facebook": {
                                            "post": True,
                                            "reel": False
                                        },
                                        "instagram": {
                                            "post": False,
                                            "story": False,
                                            "reel": True
                                        },
                                        "youtube": {
                                            "video": True,
                                            "short": False
                                        },
                                        "tiktok": True,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1920,
                                    "height": 1080,
                                    "thumbnails": media_thumbnails
                                }
                            ]
                        },
                        "youtube": {
                            "type": "video",
                            "details": {},
                            "title": video_title,
                            "text": video_desc,
                            "media": [
                                {
                                    "id": media_id,
                                    "name": None,
                                    "type": "video",
                                    "path": media_path,
                                    "validity": {
                                        "twitter": False,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": False,
                                        "facebook": {
                                            "post": True,
                                            "reel": False
                                        },
                                        "instagram": {
                                            "post": False,
                                            "story": False,
                                            "reel": True
                                        },
                                        "youtube": {
                                            "video": True,
                                            "short": False
                                        },
                                        "tiktok": True,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1920,
                                    "height": 1080,
                                    "thumbnails": media_thumbnails
                                }
                            ]
                        }
                    },
                    "accounts": [
                        {
                            "id": youtube_account,
                            "labels": [],
                            "scheduled_at": schedule_date
                        }
                    ],
                    "labels": []
                }
            ]
        }
    }


    response = requests.post(url, headers=headers, json=data, cookies=cookies)
    print(response)
    json_response = response.json()
    print(json_response)
    text_value = json_response.get("job_id", None)

    headers = {
        'authority': 'app.publer.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '',
        'publer-workspace-id': '',
        'referer': 'https://app.publer.io/',
        'sec-ch-ua': '""',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': '',
    }

    response = requests.get('https://app.publer.io/api/v1/job_status/' + text_value, headers=headers)
    print(response)
    response = response.json()
    print(response)
    if response.get('status') == 'complete':
        print("Process Completed!")
        return True

