from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class DocumentoVehiculoBase(BaseModel):
    codigo: str = Field(..., min_length=5, max_length=50, description="Código del documento")
    tipo_documento: str = Field(..., min_length=3, max_length=50, description="Tipo de documento del vehículo")
    numero_documento: str = Field(..., min_length=5, max_length=50, description="Número del documento")
    fecha_emision: Optional[date] = Field(None, description="Fecha de emisión del documento")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de vencimiento del documento")
    archivo_url: str = Field(..., min_length=5, max_length=100, description="URL del archivo del documento")
    vehiculo_id: int = Field(..., description="ID del vehículo al que pertenece el documento")

class DocumentoVehiculoCreate(DocumentoVehiculoBase):
    pass

class DocumentoVehiculo(DocumentoVehiculoBase):
    id: int = Field(..., description="ID del documento del vehículo")
    fecha_carga: datetime = Field(..., description="Fecha de carga del documento")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización del documento")

    class Config:
        from_attributes = True