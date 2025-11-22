from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class IngresoBase(BaseModel):
    tipo_ingreso: str = "VIAJE"
    descripcion: Optional[str] = None
    monto: float
    fecha: date
    cliente_cuit: Optional[str] = None
    imagen_url: Optional[str] = None

class IngresoCreate(IngresoBase):
    viaje_id: Optional[int] = None

class IngresoUpdate(IngresoBase):
    pass

class IngresoResponse(IngresoBase):
    id: int
    viaje_id: Optional[int]
    creado_en: datetime
    
    class Config:
        from_attributes = True