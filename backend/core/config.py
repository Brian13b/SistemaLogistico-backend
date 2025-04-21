from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    # Configuraciones de Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAIL_USERNAME: str 
    EMAIL_PASSWORD: str 
    EMAIL_FROM: str = "blogistic.soporte@gmail.com"

    # Google Drive
    GOOGLE_TYPE: str
    GOOGLE_PROJECT_ID: str
    GOOGLE_PRIVATE_KEY_ID: str
    GOOGLE_PRIVATE_KEY: str
    GOOGLE_CLIENT_EMAIL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_X509_CERT_URL: str

    class Config:
        env_file = ".env"

settings = Settings()