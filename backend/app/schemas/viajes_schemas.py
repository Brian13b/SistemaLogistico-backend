from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

class ViajeBase(BaseModel):
    codigo: Optional[str] = Field("", description="Código del viaje")
    origen: str = Field(..., min_length=3, max_length=50, description="Origen del viaje")
    destino: str = Field(..., min_length=3, max_length=50, description="Destino del viaje")
    vehiculo_id: int = Field(..., description="ID del vehículo asociado")
    conductor_id: int = Field(..., description="ID del conductor asociado")
    fecha_salida: date = Field(..., description="Fecha de salida del viaje")
    fecha_llegada: Optional[date] = Field(None, description="Fecha de llegada del viaje")
    producto: str = Field(..., min_length=3, max_length=50, description="Producto del viaje")
    precio: Optional[float] = Field(None, description="Precio del viaje")
    peso: Optional[float] = Field(None, description="Peso del producto transportado del viaje")
    unidad_medida: Optional[str] = Field(None, description="Unidad de medida del peso")
    estado: str = Field(..., min_length=3, max_length=50, description="Estado del viaje")

class ViajeCreate(ViajeBase):
    pass

class Viaje(ViajeBase):
    id: int = Field(..., description="ID del viaje")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del viaje")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización del viaje")

    class Config:
        from_attributes = True