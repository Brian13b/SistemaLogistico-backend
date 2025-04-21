from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from fastapi import UploadFile
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleDriveService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.service_account_info = {
            "type": os.getenv("GOOGLE_TYPE"),
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
        }
        self.credentials = service_account.Credentials.from_service_account_info(
            self.service_account_info, scopes=self.SCOPES
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
    
    async def upload_file(self, file: UploadFile, folder_id: str = None):
        file_metadata = {
            'name': file.filename,
            'mimeType': file.content_type
        }
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaIoBaseUpload(file.file, mimetype=file.content_type)
        uploaded_file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        return {
            "id": uploaded_file.get('id'),
            "name": uploaded_file.get('name'),
            "url": f"https://drive.google.com/uc?export=download&id={uploaded_file.get('id')}"
        }

drive_service = GoogleDriveService()