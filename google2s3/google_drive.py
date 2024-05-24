import io

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

class GoogleDriveClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.service = build('drive', 'v3', developerKey=api_key)

    def download_file(self, file_id):
        try:
            metadata = self.service.files().get(fileId=file_id, fields='name').execute()
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()

        except HttpError as e:
            print(f'Error: {e}')
            file = None

            return

        return metadata['name'], file.getvalue()
    