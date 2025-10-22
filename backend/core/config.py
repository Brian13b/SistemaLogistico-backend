import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL_BACKEND: str = os.getenv("DATABASE_URL_BACKEND")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = os.getenv("JWT_EXPIRE_MINUTES")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL")

    # Configuraciones de Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = os.getenv("SMTP_PORT", 587)
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "blogistic.soporte@gmail.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "izhnerkjwkhrsuwj")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "Blogistic Soporte <blogistic.soporte@gmail.com>")

    # Google Drive
    GOOGLE_TYPE: str = os.getenv("GOOGLE_TYPE")
    GOOGLE_PROJECT_ID: str = os.getenv("GOOGLE_PROJECT_ID")
    GOOGLE_PRIVATE_KEY_ID: str = os.getenv("GOOGLE_PRIVATE_KEY_ID")
    GOOGLE_PRIVATE_KEY: str = os.getenv("GOOGLE_PRIVATE_KEY")
    GOOGLE_CLIENT_EMAIL: str = os.getenv("GOOGLE_CLIENT_EMAIL")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_X509_CERT_URL: str = os.getenv("GOOGLE_CLIENT_X509_CERT_URL")


    class Config:
        env_file = ".env"

settings = Settings()