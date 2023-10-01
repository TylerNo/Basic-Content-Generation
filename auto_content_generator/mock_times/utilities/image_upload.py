import requests


def start_image_upload(file_path):
    API_URL = "https://freeimage.host/api/1/upload"
    API_KEY = ""

    headers = {
        "Authorization": API_KEY
    }

    with open(file_path, "rb") as image_file:
        files = {
            "source": image_file
        }

        payload = {
            "key": API_KEY,
            "action": "upload",
            "format": "json"
        }

        response = requests.post(API_URL, headers=headers, data=payload, files=files)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status_code") == 200:
                return json_response.get("image").get("url")
            else:
                print("Error:", json_response.get("status_txt"))
                return None
        else:
            print("HTTP Error:", response.status_code)
            return None
