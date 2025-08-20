import tempfile
import time
import os
import io
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

class GoogleDriveService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']  # Permisos para Google Drive
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
        
        # Crear directorio temporal si no existe
        self.temp_dir = "C:\\mis_archivos_temporales\\"
        os.makedirs(self.temp_dir, exist_ok=True)

    async def save_temp_file(self, upload_file: UploadFile) -> str:
        """Guardar archivo temporalmente y devolver la ruta."""
        # Lectura completa del archivo antes de escribirlo
        file_content = await upload_file.read()
        
        # Crear un nombre de archivo temporal único
        file_extension = os.path.splitext(upload_file.filename)[1]
        temp_file_path = os.path.join(
            self.temp_dir, 
            f"temp_{int(time.time())}_{os.urandom(4).hex()}{file_extension}"
        )
        
        # Escribir el contenido al archivo
        with open(temp_file_path, "wb") as f:
            f.write(file_content)
        
        # Reposicionar el upload_file para futuras lecturas
        await upload_file.seek(0)
        
        return temp_file_path

    async def upload_file_to_drive(self, file: UploadFile, folder_id: str = None):
        """Subir un archivo a Google Drive y devolver su ID y URL."""
        temp_file_path = None
        
        try:
            # Crear archivo temporal
            temp_file_path = await self.save_temp_file(file)
            
            # Metadatos del archivo
            file_metadata = {
                'name': file.filename,
                'mimeType': file.content_type
            }
            
            # Añadir a carpeta si se proporciona un folder_id
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Configurar el archivo para la subida
            media = MediaFileUpload(temp_file_path, mimetype=file.content_type, resumable=True)
            
            # Subir el archivo
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name'
            ).execute()
            
            # Dar permiso de lectura público
            self.service.permissions().create(
                fileId=uploaded_file.get('id'),
                body={
                    'type': 'anyone',
                    'role': 'reader',
                }
            ).execute()
            
            # URL para acceder directamente al archivo
            file_url = f"https://drive.google.com/uc?id={uploaded_file.get('id')}"
            
            return {
                "drive_id": uploaded_file.get('id'),
                "name": uploaded_file.get('name'),
                "url": file_url
            }
        
        except Exception as e:
            raise e
        
        finally:
            # Liberamos recursos sin importar lo que suceda
            # Esperar un momento antes de intentar eliminar el archivo
            await asyncio.sleep(0.5)
            
            # Intentar eliminar el archivo temporal con manejo de errores
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    # print(f"No se pudo eliminar el archivo temporal {temp_file_path}: {str(e)}")
                    # Programar eliminación para más tarde (opcional)
                    self._schedule_file_deletion(temp_file_path)
    
    def _schedule_file_deletion(self, file_path, retries=3, delay=2):
        """Programa un intento de eliminación de archivo para más tarde"""
        def delete_later():
            for i in range(retries):
                time.sleep(delay)
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        # print(f"Archivo temporal eliminado con éxito en intento {i+1}: {file_path}")
                        break
                except Exception as e:
                    if i == retries - 1:
                        # print(f"No se pudo eliminar el archivo temporal después de {retries} intentos: {file_path}")
                        pass
        # Iniciar un thread para manejar la eliminación
        import threading
        threading.Thread(target=delete_later, daemon=True).start()
    
    async def download_file_from_drive(self, file_id: str):
        """Descargar un archivo de Google Drive por su ID."""
        request = self.service.files().get_media(fileId=file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        file_content.seek(0)
        return file_content
    
    def get_file_info(self, file_id: str):
        """Obtener información sobre un archivo de Google Drive."""
        return self.service.files().get(fileId=file_id, fields='name,mimeType').execute()

# Instancia singleton del servicio
drive_service = GoogleDriveService()