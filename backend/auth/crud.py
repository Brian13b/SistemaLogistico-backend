from datetime import datetime, timedelta
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.usuario import User
from auth.schemas import UserCreate
from auth.security import get_password_hash, verify_password
from core.config import settings


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session) -> List[User]:
    return db.query(User).all()

def update_user(db: Session, username:str, update_data: dict) -> User:
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, usernane: str):
    db_user = get_user_by_username(db, usernane)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    db.delete(db_user)
    db.commit()
    return db_user

def create_password_reset_token(db: Session, email: str) -> Optional[str]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    reset_token = secrets.token_urlsafe(32)
    
    user.reset_token = reset_token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(hours=1)
    
    db.commit()
    db.refresh(user)
    
    return reset_token

def reset_password(db: Session, email: str, reset_token: str, new_password: str) -> Dict[str, str]:
    user = db.query(User).filter(
        User.email == email,
        User.reset_token == reset_token,
        User.reset_token_expires_at > datetime.utcnow()
    ).first()
    
    if not user:
        return {"success": False, "message": "Token inválido o expirado"}
    
    if verify_password(new_password, user.hashed_password):
        return {"success": False, "message": "La nueva contraseña no puede ser igual a la anterior"}
    
    hashed_password = get_password_hash(new_password)
    
    user.hashed_password = hashed_password
    user.reset_token = None
    user.reset_token_expires_at = None
    
    db.commit()
    return {"success": True, "message": "Contraseña restablecida exitosamente"}

def send_password_reset_email(to_email: str, reset_link: str) -> Dict[str, bool]:
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = "Recuperación de Contraseña"

        body_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h2>Recuperación de Contraseña</h2>
            <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
            <p>Haz clic en el siguiente enlace para cambiar tu contraseña:</p>
            <a href="{reset_link}">Restablecer Contraseña</a>
            <p>Si no solicitaste este cambio, ignora este correo.</p>
            <small>El enlace expirará en 1 hora.</small>
        </body>
        </html>
        """
        
        part = MIMEText(body_html, 'html', 'utf-8')
        msg.attach(part)

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.set_debuglevel(1)
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            
            server.sendmail(
                settings.EMAIL_FROM, 
                to_email, 
                msg.as_string()
            )
        
        return {"success": True, "message": "Correo enviado exitosamente"}
    except Exception as e:
        print(f"Error al enviar correo de recuperación: {e}")
        return {"success": False, "message": str(e)}