import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Function to authenticate with Google Drive API
def authenticate_with_google_drive(client_config):
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Load OAuth credentials from a file
    creds = None
    if os.path.exists('credentials.json'):
        creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
    
    # If credentials are not found or are invalid, initiate the OAuth flow to obtain new credentials
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save the credentials for future use
    with open('credentials.json', 'w') as credentials_file:
        credentials_file.write(creds.to_json())
    
    return creds

# Function to list files in a Google Drive folder
def list_files_in_folder(folder_id, client_config):
    # Authenticate with Google Drive API
    creds = authenticate_with_google_drive(client_config)
    service = build('drive', 'v3', credentials=creds)

    # List files in the specified folder
    results = service.files().list(q=f"'{folder_id}' in parents", pageSize=10, fields="nextPageToken, files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found in the folder.')
    else:
        print('Files in the folder:')
        for file in files:
            print(f'{file["name"]} ({file["id"]})')

# OAuth 2.0 client configuration
client_config = {
  "installed": {
    "client_id": "38484099262-7ut7lc9b9bat4jng34kouviocgqicdag.apps.googleusercontent.com",
    "project_id": "myprojectai-420706",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["http://localhost"]
  }
}

# Folder ID of the folder in Google Drive
folder_id = '1XRfdSIle1WPrcmXS5kwbycN7tdIHJPlE'

# Call the function to list files in the specified folder
list_files_in_folder(folder_id, client_config)
