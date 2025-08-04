from datetime import datetime
import os
import webbrowser

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Config ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'client_secret_202152707893-f1i3ikivf25nt6d69cag3fbr6rk3eoar.apps.googleusercontent.com.json'
TOKEN_FILE = 'token.json'
TXT_FILE = 'current_time.txt'

# --- Save Current Time ---
def save_current_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TXT_FILE, "w") as f:
        f.write(f"Current time: {now}")

# --- Authenticate with Chrome ---
def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Register Chrome browser
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Update if Chrome is installed elsewhere
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0, browser='chrome')

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

# --- Upload File to Drive ---
def upload_to_drive(creds):
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': TXT_FILE}
    media = MediaFileUpload(TXT_FILE, mimetype='text/plain')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Uploaded to Google Drive. File ID: {file.get('id')}")

# --- Main ---
if __name__ == '__main__':
    save_current_time()
    creds = authenticate()
    upload_to_drive(creds)
