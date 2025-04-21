from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class ConductorBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=10, description="Código del conductor")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del conductor")
    apellido: str = Field(..., min_length=3, max_length=50, description="Apellido del conductor")
    dni: str = Field(..., min_length=8, max_length=8, description="DNI del conductor")
    foto: Optional[str] = Field(None, description="Foto del conductor")
    numero_contacto: Optional[str] = Field(None, min_length=9, max_length=11, description="Número de contacto del conductor")
    email_contacto: Optional[str] = Field(None, max_length=50, description="Email de contacto del conductor")
    direccion: str = Field(..., max_length=50, description="Dirección del conductor")
    estado: str = Field("Activo", description="Estado del conductor")

class ConductorCreate(ConductorBase):
    pass

class Conductor(ConductorBase):
    id: int = Field(..., description="ID del conductor")
    creado_en: datetime = Field(..., description="Fecha de creación del conductor")
    actualizado_en: datetime = Field(..., description="Fecha de actualización del conductor")

    class Config:
        from_attributes = True