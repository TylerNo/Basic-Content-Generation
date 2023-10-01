from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import time
from datetime import datetime, timedelta
import json

def upload_file(file_name, file_path, mime_type):
    print("Starting video upload to Google Drive")

    folder_id = ""
    creds = Credentials.from_service_account_file(
        "auto_content_generator/core/assets/credentials.json",
        scopes=["https://www.googleapis.com/auth/drive.file"])
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name, 'parents': [folder_id]}

    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    request = service.files().create(media_body=media, body=file_metadata)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")

    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=response['id'], body=permission).execute()

    uploaded_file_link = f"https://drive.google.com/file/d/{response['id']}/view"
    print(f'Uploaded file {response["name"]} with id {response["id"]}')
    print(f'Sharing link: {uploaded_file_link}')

    return uploaded_file_link


def start_video_uploader(config, log_manager, app_logs, MAX_LOG_ENTRIES, legal_fact):
    log_message = "Starting Fact Drip Video Uploader..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    uploaded_file = upload_file('legal_output_video.mp4',
                                'auto_content_generator/fact_drip/assets/temp/legal_output_video.mp4',
                                'video/mp4')
    time.sleep(5)
    print(uploaded_file)

    fact_pt1 = legal_fact[3] + "..."
    youtube_account = ""

    link = uploaded_file

    current_time = datetime.now()

    base_scheduled_time = current_time + timedelta(hours=5)

    schedule_date = base_scheduled_time.strftime('%Y-%m-%dT%H:%M') + "-07:00"
    print(schedule_date)


    video_desc = '#dailyfacts #factshorts #legalfacts'
    link = uploaded_file


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
        "sec-ch-ua": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "",
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

    while True:
        response = requests.get(url, headers=headers)
        print(response)
        response_data = response.json()
        print(response_data)

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

    print(media_thumbnails)
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
                            "details": {
                                "type": "short"
                            },
                            "title": fact_pt1 + " #legal #law #facts",
                            "text": video_desc,
                            "media": [
                                {
                                    "id": media_id,
                                    "name": None,
                                    "type": "video",
                                    "path": media_path,
                                    "validity": {
                                        "twitter": True,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": False,
                                        "facebook": {
                                            "post": True,
                                            "reel": True
                                        },
                                        "instagram": {
                                            "post": True,
                                            "story": True,
                                            "reel": True
                                        },
                                        "youtube": {
                                            "video": True,
                                            "short": True
                                        },
                                        "tiktok": True,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1080,
                                    "height": 1920,
                                    "caption": "",
                                    "thumbnails": media_thumbnails
                                }
                            ]
                        },
                        "youtube": {
                            "type": "video",
                            "details": {
                                "type": "short"
                            },
                            "title": fact_pt1 + " #legal #law #facts",
                            "text": video_desc,
                            "media": [
                                {
                                    "id": media_id,
                                    "name": None,
                                    "type": "video",
                                    "path": media_path,
                                    "validity": {
                                        "twitter": True,
                                        "linkedin": True,
                                        "pinterest": True,
                                        "google": False,
                                        "facebook": {
                                            "post": True,
                                            "reel": True
                                        },
                                        "instagram": {
                                            "post": True,
                                            "story": True,
                                            "reel": True
                                        },
                                        "youtube": {
                                            "video": True,
                                            "short": True
                                        },
                                        "tiktok": True,
                                        "telegram": True,
                                        "wordpress_basic": True,
                                        "wordpress_oauth": True
                                    },
                                    "width": 1080,
                                    "height": 1920,
                                    "caption": "",
                                    "thumbnails": media_thumbnails
                                }
                            ]
                        }
                    },
                    "accounts": [
                        {
                            "id": youtube_account,
                            "previewed_link": False,
                            "previewed_media": False,
                            "labels": [],
                            "scheduled_at": schedule_date
                        }
                    ],
                    "labels": []
                }
            ]
        }
    }




    response = requests.post(url, headers=headers, json=data)
    print(response.text)

    if response.status_code == 200:
        print("Request was successful!")
        try:
            response_data = response.json()
            job_id = response_data.get("job_id")
            print(json.dumps(response_data, indent=4))
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print(f"Failed to make the request. Status code: {response.status_code}")
        print(response.text)

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

    while True:
        response = requests.get('https://app.publer.io/api/v1/job_status/' + job_id, headers=headers)
        print(response)
        response = response.json()
        print(response)
        if response.get('status') == 'complete':
            print("Process Complete!")
            return "Yes"
        time.sleep(3)

