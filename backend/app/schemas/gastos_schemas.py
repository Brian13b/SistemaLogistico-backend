from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class GastoBase(BaseModel):
    nombre: str = Field(..., max_length=50, description="Nombre del gasto")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción del gasto")
    monto: float = Field(..., gt=0, description="Monto del gasto")
    fecha: str = Field(..., pattern=r"^\d{2}-\d{2}-\d{4}$", description="Fecha en formato DD-MM-YYYY")
    imagen_url: Optional[str] = Field(None, max_length=200, description="URL de la imagen del gasto")
    viaje_id: int = Field(..., description="ID del viaje asociado al gasto")

class GastoCreate(GastoBase):
    pass

class Gasto(GastoBase):
    id: int = Field(..., description="ID del gasto")
    creado_en: datetime = Field(..., description="Fecha de creación del gasto")
    actualizado_en: datetime = Field(..., description="Fecha de actualización del gasto")

    class Config:
        from_attributes = True