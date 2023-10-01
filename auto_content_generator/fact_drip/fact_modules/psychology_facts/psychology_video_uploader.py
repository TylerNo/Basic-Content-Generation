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


def start_video_uploader(config, log_manager, app_logs, MAX_LOG_ENTRIES, psychology_fact):
    log_message = "Starting Fact Drip Video Uploader..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    uploaded_file = upload_file('psychology_output_video.mp4',
                                'auto_content_generator/fact_drip/assets/temp/psychology_output_video.mp4',
                                'video/mp4')
    time.sleep(5)
    print(uploaded_file)

    fact_pt1 = psychology_fact[3] + "..."
    youtube_account = ""

    link = uploaded_file

    current_time = datetime.now()

    base_scheduled_time = current_time + timedelta(hours=5)

    schedule_date = base_scheduled_time.strftime('%Y-%m-%dT%H:%M') + "-07:00"
    print(schedule_date)


    video_desc = '#dailyfacts #factshorts #psychologyfacts'
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






    media_payload = response_data['payload'][0]  # Assuming the first item in the payload list
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
        "cookie": "timezone=America%2FLos_Angeles; is_military=false; week_starts_on_monday=true; start_day_at=00%3A00+%28midnight%29; policy=true; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc2lOalJsTURJd09UVmtZakkzT1RjNU16RTRaalUxTlRobElsMHNJaVF5WVNReE1TUldOMEZ0TTFreFQyOTVZMDA1VEZabFJtNVhjRzB1SWl3aU1UWTVNalF4TXpRME1pNHhORE15TXpZNUlsMD0iLCJleHAiOiIyMDI0LTA4LTE5VDAyOjUwOjQyLjE0M1oiLCJwdXIiOm51bGx9fQ%3D%3D--9ec00d4d2fdf3e2e0799b6aedc1d2c9d4afce8b3; browser_id=e7bc01fe3498d9d4dc0bd416ba6c3f97; listView=true; publer_calendar_default_calendarView=%22week%22; workspace=64e020d9db279792c3f546f7; feedFilter=0; publer_calendar_default_selectedDate=%22Sun+Sep+03+2023+21:03:29+GMT-0700%22; feedType=failed; spotlightSeen=https://publer.io/blog/use-x-twitter-for-free/; user=%7B%22id%22%3A%2264e02095db27979318f5558e%22%2C%22email%22%3A%22contact%40tylernorman.com%22%2C%22name%22%3A%22Tyler+Norman%22%2C%22picture%22%3A%22https%3A%2F%2Fcdn.publer.io%2Fuploads%2Fphotos%2Fthumb_64e02095db27979318f5558e.png%3Fv%3D154d7ae3604c8030c46b%22%2C%22has_vista%22%3Anull%2C%22subscribed%22%3Atrue%2C%22unread_notifications%22%3A0%2C%22workspace%22%3A%2264e020d9db279792c3f546f7%22%2C%22can_migrate%22%3Afalse%2C%22can_discount%22%3Afalse%2C%22persona%22%3A%7B%22role%22%3A%22Other%22%2C%22source%22%3A%22Google%22%2C%22goal%22%3A%22Other.%22%7D%2C%22ambassador%22%3Anull%2C%22pending_invitation%22%3Afalse%2C%22canva_user_id%22%3Afalse%2C%22open_ai_key%22%3Afalse%2C%22has_2fa%22%3Afalse%7D; crisp-client%2Fsession%2F7d49334f-826f-4228-9f8b-46b9c8fc6cc4=session_4798210c-f15c-49bf-93e5-8f287db1a993; crisp-client%2Fsession%2F7d49334f-826f-4228-9f8b-46b9c8fc6cc4%2F64e02095db27979318f5558e=session_4798210c-f15c-49bf-93e5-8f287db1a993; token=YjJSOWJwTERpSmJjUGlaUG5rL0UzbGcyQnlid0cxUzJIYkNlWFcya29jY0MyZEgrWSs3cUVnK25DeGdvbjdnNlh3b2s2NTkzaEx5UmU2dHdubXJwZWswRlhQTVkxbUlQN2FPSndLTVI2cFZkMmkyVGppREhBNzRNWVlQaCtqcEprWDlzaFpPOVg4TlNNQU04K3AxeGJUcmVDWmdpUHBNMktvLzhVQVIvOUEwPS0tUHBaVWxCaThPMGpwZDZ2Y1BFMllGZz09--f7ffa9cb31a4f17da9e48dc3dbf610f5df7af7a3; _publer_session=YXc0YXpBWHJvK1A5R0JVRXh3c2o3cVNWT3kxVU1JNy9pNnBoYmJQbS9HQXA5dHdVWkFPa1FCQW50WTlXNUpNSWEvaWZ3TXV3SnpIdlNsQVJwU3RhM3FkYXREd2gwWHgwQVJTVUZiRXlCaVk1Qi8zZUs2cHB6bU92SEI4QUJvb2xBbHVtYnR5QTJ6ejRjVWhIZ1grb2s2aWVtdDVFSnlhRmhRazdqdWQxRmFSL1VlVmNwMDBPYzJIUE1YVmpXRGp5OGpZcUhoVGJJbWFXRG1ST3dwUFNrQ1BXY090ZEEyaVQ0Z2N0S3BQRzVOaVFIQUdRUGN0UEZhUUJiL2J3emJISzBmc3liRWxtTzNrVXM0YlVobEU1UDhTd0VKa0M2ZkhxeEd2cis4dWNKU3ZVYy9lZkR6TnFsRTFWcCtqbDV2V2JrUW9nK2x2OThlK1h0UEc4RVhHcHBBPT0tLVlXUmllRkhweXpsMlZZNVpmVS9ndEE9PQ%3D%3D--cf1cbf75472391317d663d62770493ed1a335edb; lastScheduled=2023-09-07T11:37-07:00",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "64e020d9db279792c3f546f7",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
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
                            "title": fact_pt1 + " #psychology #facts",
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
                            "title": fact_pt1 + " #psychology #facts",
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
        "cookie": "timezone=America%2FLos_Angeles; is_military=false; week_starts_on_monday=true; start_day_at=00%3A00+%28midnight%29; policy=true; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc2lOalJsTURJd09UVmtZakkzT1RjNU16RTRaalUxTlRobElsMHNJaVF5WVNReE1TUldOMEZ0TTFreFQyOTVZMDA1VEZabFJtNVhjRzB1SWl3aU1UWTVNalF4TXpRME1pNHhORE15TXpZNUlsMD0iLCJleHAiOiIyMDI0LTA4LTE5VDAyOjUwOjQyLjE0M1oiLCJwdXIiOm51bGx9fQ%3D%3D--9ec00d4d2fdf3e2e0799b6aedc1d2c9d4afce8b3; browser_id=e7bc01fe3498d9d4dc0bd416ba6c3f97; listView=true; publer_calendar_default_calendarView=%22week%22; workspace=64e020d9db279792c3f546f7; feedFilter=0; publer_calendar_default_selectedDate=%22Sun+Sep+03+2023+21:03:29+GMT-0700%22; feedType=failed; spotlightSeen=https://publer.io/blog/use-x-twitter-for-free/; user=%7B%22id%22%3A%2264e02095db27979318f5558e%22%2C%22email%22%3A%22contact%40tylernorman.com%22%2C%22name%22%3A%22Tyler+Norman%22%2C%22picture%22%3A%22https%3A%2F%2Fcdn.publer.io%2Fuploads%2Fphotos%2Fthumb_64e02095db27979318f5558e.png%3Fv%3D154d7ae3604c8030c46b%22%2C%22has_vista%22%3Anull%2C%22subscribed%22%3Atrue%2C%22unread_notifications%22%3A0%2C%22workspace%22%3A%2264e020d9db279792c3f546f7%22%2C%22can_migrate%22%3Afalse%2C%22can_discount%22%3Afalse%2C%22persona%22%3A%7B%22role%22%3A%22Other%22%2C%22source%22%3A%22Google%22%2C%22goal%22%3A%22Other.%22%7D%2C%22ambassador%22%3Anull%2C%22pending_invitation%22%3Afalse%2C%22canva_user_id%22%3Afalse%2C%22open_ai_key%22%3Afalse%2C%22has_2fa%22%3Afalse%7D; crisp-client%2Fsession%2F7d49334f-826f-4228-9f8b-46b9c8fc6cc4=session_4798210c-f15c-49bf-93e5-8f287db1a993; crisp-client%2Fsession%2F7d49334f-826f-4228-9f8b-46b9c8fc6cc4%2F64e02095db27979318f5558e=session_4798210c-f15c-49bf-93e5-8f287db1a993; token=YjJSOWJwTERpSmJjUGlaUG5rL0UzbGcyQnlid0cxUzJIYkNlWFcya29jY0MyZEgrWSs3cUVnK25DeGdvbjdnNlh3b2s2NTkzaEx5UmU2dHdubXJwZWswRlhQTVkxbUlQN2FPSndLTVI2cFZkMmkyVGppREhBNzRNWVlQaCtqcEprWDlzaFpPOVg4TlNNQU04K3AxeGJUcmVDWmdpUHBNMktvLzhVQVIvOUEwPS0tUHBaVWxCaThPMGpwZDZ2Y1BFMllGZz09--f7ffa9cb31a4f17da9e48dc3dbf610f5df7af7a3; _publer_session=YXc0YXpBWHJvK1A5R0JVRXh3c2o3cVNWT3kxVU1JNy9pNnBoYmJQbS9HQXA5dHdVWkFPa1FCQW50WTlXNUpNSWEvaWZ3TXV3SnpIdlNsQVJwU3RhM3FkYXREd2gwWHgwQVJTVUZiRXlCaVk1Qi8zZUs2cHB6bU92SEI4QUJvb2xBbHVtYnR5QTJ6ejRjVWhIZ1grb2s2aWVtdDVFSnlhRmhRazdqdWQxRmFSL1VlVmNwMDBPYzJIUE1YVmpXRGp5OGpZcUhoVGJJbWFXRG1ST3dwUFNrQ1BXY090ZEEyaVQ0Z2N0S3BQRzVOaVFIQUdRUGN0UEZhUUJiL2J3emJISzBmc3liRWxtTzNrVXM0YlVobEU1UDhTd0VKa0M2ZkhxeEd2cis4dWNKU3ZVYy9lZkR6TnFsRTFWcCtqbDV2V2JrUW9nK2x2OThlK1h0UEc4RVhHcHBBPT0tLVlXUmllRkhweXpsMlZZNVpmVS9ndEE9PQ%3D%3D--cf1cbf75472391317d663d62770493ed1a335edb; lastScheduled=2023-09-07T11:37-07:00",
        "origin": "https://app.publer.io",
        "publer-workspace-id": "64e020d9db279792c3f546f7",
        "referer": "https://app.publer.io/",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    while True:
        response = requests.get('https://app.publer.io/api/v1/job_status/' + job_id, headers=headers)
        print(response)
        response = response.json()
        print(response)
        if response.get('status') == 'complete':
            print("Process Complete!")
            return "Yes"

        # Pause for a short period to avoid hitting the server too quickly
        time.sleep(3)

