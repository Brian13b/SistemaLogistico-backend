from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IngresoBase(BaseModel):
    descripcion: str = Field(..., max_length=200, description="Descripción del ingreso")
    monto: float = Field(..., gt=0, description="Monto del ingreso")
    fecha: str = Field(..., pattern=r"^\d{2}-\d{2}-\d{4}$", description="Fecha en formato DD-MM-YYYY")
    imagen_url: Optional[str] = Field(None, max_length=200, description="URL de la imagen del ingreso")
    viaje_id: int

class IngresoCreate(IngresoBase):
    pass

class Ingreso(IngresoBase):
    id: int = Field(..., description="ID del ingreso")
    creado_en: datetime = Field(..., description="Fecha de creación del ingreso")
    actualizado_en: datetime = Field(..., description="Fecha de actualización del ingreso")

    class Config:
        from_attributes = True