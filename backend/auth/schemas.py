from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from auth.usuario import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.CONDUCTOR

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    email: Optional[EmailStr] = None 
    token: str
    new_password: str = Field(
        ..., 
        min_length=8, 
        description="La contraseña debe tener al menos 8 caracteres"
    )
    confirm_password: str = Field(
        ..., 
        min_length=8, 
        description="Debe coincidir con la nueva contraseña"
    )

    class Config:
        from_attributes = True