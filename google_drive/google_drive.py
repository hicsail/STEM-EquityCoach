import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

from utils import is_compressed_file

class GoogleDriveClient:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_CREDS_PATH'))
        self.service = build('drive', 'v3', credentials=credentials)

    # get all file ids in a folder recuesively. ignore folders. also ignore files with certain extensions
    def get_file_ids(self, folder_id, ignore_ext=[]):
        try:
            query = f"'{folder_id}' in parents"
            response = self.service.files().list(q=query, fields='files(id, name, mimeType)').execute()
            files = response.get('files', [])

            file_ids = []
            compressed_ids = []
            for file in files:
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    files, compressed = self.get_file_ids(file['id'], ignore_ext)
                    file_ids.extend(files)
                    compressed_ids.extend(compressed)
                else:
                    if not any(file['name'].endswith(f'.{ext}') for ext in ignore_ext):
                        if is_compressed_file(file['mimeType']):
                            compressed_ids.append(file['id'])
                        else:
                            file_ids.append(file['id'])

            return file_ids, compressed_ids

        except HttpError as e:
            print(f'Error: {e}')
            return [], []

    def download_file(self, file_id, dest=None):
        if dest is None:
            dest = os.getenv('DOWNLOAD_PATH')
        try:
            metadata = self.service.files().get(fileId=file_id, fields='name').execute()
            request = self.service.files().get_media(fileId=file_id)
            file_path = os.path.join(dest, metadata['name'])
            os.makedirs(dest, exist_ok=True)
            os.chmod(dest, 0o755)

            with open(file_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                print(f'Downloading {metadata["name"]}...')

                while not done:
                    _, done = downloader.next_chunk()

            print(f'Download complete')
            return file_path, metadata

        except HttpError as e:
            print(f'Error: {e}')
            
            return None
    