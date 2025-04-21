from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class VehiculoBase(BaseModel):
    codigo: Optional[str] = Field(None, max_length=50, description="Código del vehículo")
    marca: str = Field(..., min_length=3, max_length=50, description="Marca del vehículo")
    modelo: str = Field(..., min_length=3, max_length=50, description="Modelo del vehículo")
    patente: str = Field(..., min_length=5, max_length=10, description="Patente del vehículo")
    anio: int = Field(..., description="Año del vehículo")
    tipo: str = Field(..., min_length=3, max_length=50, description="Tipo del vehículo")
    tara: int = Field(..., description="Tara del vehículo")
    carga_maxima: int = Field(..., description="Carga máxima del vehículo")
    estado: str = Field(..., max_length=50, description="Estado del vehículo")
    kilometraje: float = Field(..., description="Kilometraje del vehículo")
    id_conductor: Optional[int] = Field(None, description="ID del conductor asociado")

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id: int = Field(..., description="ID del vehículo")
    fecha_alta: datetime = Field(..., description="Fecha de alta del vehículo")
    fecha_baja: Optional[datetime] = Field(None, description="Fecha de baja del vehículo") 
    fecha_actualizacion: datetime = Field(None, description="Fecha de actualizacion del vehículo")

    class Config:
        from_attributes = True