from pydantic import BaseModel
from typing import Optional
from datetime import date

class GastoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    monto: float
    fecha: date
    tipo_gasto: str = "GENERAL" 
    imagen_url: Optional[str] = None

class GastoCreate(GastoBase):
    viaje_id: Optional[int] = None
    vehiculo_id: Optional[int] = None
    conductor_id: Optional[int] = None

class GastoResponse(GastoBase):
    id: int
    viaje_id: Optional[int]
    vehiculo_id: Optional[int]
    conductor_id: Optional[int]
    
    class Config:
        from_attributes = True