from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


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

