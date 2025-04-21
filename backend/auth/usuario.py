from sqlalchemy import Column, DateTime, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CONDUCTOR = "CONDUCTOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CONDUCTOR)
    reset_token: str = Column(String, nullable=True)
    reset_token_expires_at: DateTime = Column(DateTime(timezone=True), nullable=True)