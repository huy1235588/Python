from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'google_drive/json/ethereal-runner-430705-j1-4a67cbafb0fc.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

folder_id = '1EO4svG96F2SpDyvb46t4pYnUnOpdiecairMbThwZ91lNEE_lv6nT6qnkF2xPIb7YwlyUck2e'  # Thay bằng ID của thư mục bạn muốn kiểm tra

def get_folder_size(service, folder_id):
    total_size = 0
    query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
    page_token = None
    while True:
        response = service.files().list(q=query, fields="nextPageToken, files(size)", pageToken=page_token).execute()
        for file in response.get('files', []):
            total_size += int(file.get('size', 0))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return total_size


def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    page_token = None
    while True:
        response = service.files().list(q=query, fields="nextPageToken, files(name, size)", pageToken=page_token).execute()
        files = response.get('files', [])
        if not files:
            print("No files found.")
        for file in files:
            print(f"File: {file.get('name')}, Size: {file.get('size')}")
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

list_files_in_folder(service, folder_id)

# size_in_bytes = get_folder_size(service, folder_id)
# print(f"Folder size: {size_in_bytes / (1024 ** 3):.2f} GB")
# print(f"Folder size: {size_in_bytes} KB")
