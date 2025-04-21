import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fastapi import FastAPI
from auth.usuario_controller import router as auth_router
from app.controllers import conductores_controller, vehiculos_controller, viajes_controller, documentos_conductores_controller, documentos_vehiculos_controller, documentos_viajes_controller
from app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "monokai"}})

create_tables()

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(conductores_controller.router, prefix="/api", tags=["Conductores"])
app.include_router(documentos_conductores_controller.router, prefix="/api", tags=["Documentos Conductores"])
app.include_router(vehiculos_controller.router, prefix="/api", tags=["Vehiculos"])
app.include_router(documentos_vehiculos_controller.router, prefix="/api", tags=["Documentos Vehiculos"])
app.include_router(viajes_controller.router, prefix="/api", tags=["Viajes"])
app.include_router(documentos_viajes_controller.router, prefix="/api", tags=["Documentos Viajes"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ['https://www.googleapis.com/auth/drive.file']

SERVICE_ACCOUNT_INFO = {
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

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)