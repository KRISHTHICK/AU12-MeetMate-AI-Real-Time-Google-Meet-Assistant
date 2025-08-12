# google_drive.py
import os, io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate(credentials_json='credentials.json', token_path='token.json'):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
    return creds

def list_recordings_for_meet(creds, meet_code=None, folder_id=None):
    service = build('drive', 'v3', credentials=creds)
    q_parts = []
    # If folder id provided, search inside it
    if folder_id:
        q_parts.append(f"'{folder_id}' in parents")
    # Filter video files (Google Meet recordings are stored as Google Drive files with mimeType video/* or application/octet-stream)
    q_parts.append("mimeType contains 'video/'")
    if meet_code:
        # search name contains the meet code (user may use meeting title)
        q_parts.append(f"name contains '{meet_code}'")
    q = " and ".join(q_parts)
    results = service.files().list(q=q, pageSize=50, fields="files(id, name, mimeType, createdTime)").execute()
    return results.get('files', [])

def download_file(creds, file_id, dest_path):
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return dest_path
