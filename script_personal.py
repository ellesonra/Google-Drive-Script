import os
import io
import json
import pickle
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']  # No restricted scope
local_path = os.path.join(os.getcwd(), "exports")

if not os.path.exists(local_path):
    os.makedirs(local_path)

def get_google_auth_user_info():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    creds_json = creds.to_json()
    return json.loads(creds_json)

def sanitize_filename(filename):
    return filename.replace('<', '-').replace('>', '-').replace(':', '-').replace('"', '-').replace('/', '-').replace('\\', '-').replace('|', '-').replace('?', '-').replace('*', '-').replace('(', '-').replace(')', '-').replace(',', '-')

def download_file(drive_service, file_id, file_name, local_folder_path, mime_type):
    file_name = sanitize_filename(file_name)

    google_mime_map = {
        'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
        'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
        'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
    }

    if mime_type in google_mime_map:
        mime_type_export, file_extension = google_mime_map[mime_type]
        request = drive_service.files().export_media(fileId=file_id, mimeType=mime_type_export)
    else:
        file_extension = '.' + mime_type.split('/')[-1].split(';')[0] if '/' in mime_type else '.bin'
        request = drive_service.files().get_media(fileId=file_id)

    file_name = os.path.splitext(file_name)[0] + file_extension
    file_path = os.path.join(local_folder_path, file_name)

    if os.path.exists(file_path):
        print(f"File already exists, skipping download: {file_path}")
        return

    try:
        file_data = io.BytesIO()
        downloader = MediaIoBaseDownload(file_data, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        with open(file_path, 'wb') as f:
            f.write(file_data.getvalue())
        print(f"File saved: {file_path}")
    except Exception as e:
        print(f"Failed to download {file_name}. Error: {str(e)}")

def download_files_in_folder(drive_service, folder_id, local_folder_path):
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])
    for item in items:
        file_id = item['id']
        file_name = item['name']
        mime_type = item['mimeType']
        if mime_type == 'application/vnd.google-apps.folder':
            new_folder_path = os.path.join(local_folder_path, sanitize_filename(file_name))
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            download_files_in_folder(drive_service, file_id, new_folder_path)
        else:
            download_file(drive_service, file_id, file_name, local_folder_path, mime_type)

def download_personal_drive_folder(folder_id):
    creds = Credentials.from_authorized_user_info(info=get_google_auth_user_info())
    drive_service = build('drive', 'v3', credentials=creds)
    download_files_in_folder(drive_service, folder_id, local_path)

if __name__ == "__main__":
    folder_id = input("Enter your personal Google Drive Folder ID: ")
    download_personal_drive_folder(folder_id)
