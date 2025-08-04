import os
import json
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Config ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TXT_FILE = 'current_time.txt'

# --- Save current time to a file ---
def save_current_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TXT_FILE, "w") as f:
        f.write(f"Current time: {now}")

# --- Authenticate using token from GitHub secret ---
def authenticate():
    token_data = os.environ.get("TOKEN_JSON")
    if not token_data:
        print("❌ TOKEN_JSON secret not found.")
        exit(1)
    creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
    return creds

# --- Upload the file to Google Drive ---
def upload_to_drive(creds):
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': TXT_FILE}
    media = MediaFileUpload(TXT_FILE, mimetype='text/plain')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Uploaded to Google Drive. File ID: {file.get('id')}")

# --- Main script ---
if __name__ == '__main__':
    save_current_time()
    creds = authenticate()
    upload_to_drive(creds)
