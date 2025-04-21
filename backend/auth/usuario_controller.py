from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, List

from app.database.database import get_db
from auth.schemas import PasswordResetConfirm, PasswordResetRequest, UserCreate, Token, UserResponse, UserUpdate, UserAdminUpdate
from auth.crud import create_password_reset_token, create_user, delete_user, get_user_by_email, get_user_by_username, list_users, reset_password, send_password_reset_email, update_user
from auth.security import get_password_hash, verify_password, create_access_token
from auth.dependencies import get_current_user, require_role
from auth.usuario import UserRole
from core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(require_role(UserRole.ADMINISTRADOR))):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, 
            detail="Usuario o contraaseña incorrectos"
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/users/{username}", response_model=UserResponse)
def update_user_details(username: str, user_update: UserAdminUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(require_role(UserRole.ADMINISTRADOR))):
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)

    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

    return update_user(db, username, update_data)

@router.put("/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    if user_update.new_password:
        if not verify_password(user_update.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Contraseña actual incorrecta"
            )
        
        hashed_password = get_password_hash(user_update.new_password)
    else:
        hashed_password = None

    update_data = {
        "username": user_update.username or current_user.username,
        "email": user_update.email or current_user.email,
        "hashed_password": hashed_password
    }

    return update_user(db, current_user.username, update_data)

@router.get("/users", response_model=List[UserResponse])
def list_all_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(require_role(UserRole.ADMINISTRADOR))):
    return list_users(db)

@router.get("/users/{username}", response_model=UserResponse)
def get_user_details(username: str, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    return db_user

@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(username: str, db: Session = Depends(get_db), current_user: UserResponse = Depends(require_role(UserRole.ADMINISTRADOR))):
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    if db_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No puedes eliminarte a ti mismo"
        )

    delete_user(db, username)
    return None

@router.post("/request-password-reset")
def solicitar_recuperacion_contrasena(solicitud_recuperacion: PasswordResetRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    usuario = get_user_by_email(db, solicitud_recuperacion.email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró ningún usuario con este correo electrónico"
        )
    
    token_recuperacion = create_password_reset_token(db, solicitud_recuperacion.email)
    
    if not token_recuperacion:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo generar el token de recuperación"
        )
    
    enlace_recuperacion = f"{settings.FRONTEND_URL}/reset-password?token={token_recuperacion}&email={solicitud_recuperacion.email}"
    
    resultado_correo = send_password_reset_email(usuario.email, enlace_recuperacion)
    
    if not resultado_correo['success']:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo enviar el correo de recuperación"
        )
    
    return {
        "mensaje": "Se ha enviado un enlace de recuperación de contraseña a su correo electrónico"
    }

@router.post("/reset-password")
def recuperar_contrasena(datos_recuperacion: PasswordResetConfirm, db: Session = Depends(get_db)) -> Dict[str, str]:

    if datos_recuperacion.new_password != datos_recuperacion.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Las contraseñas no coinciden"
        )
    
    resultado = reset_password(
        db, 
        datos_recuperacion.email,
        datos_recuperacion.token, 
        datos_recuperacion.new_password
    )
    
    if not resultado['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=resultado['message']
        )
    
    return {
        "mensaje": resultado['message']
    }