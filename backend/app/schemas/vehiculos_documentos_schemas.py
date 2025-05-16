from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class DocumentoVehiculoBase(BaseModel):
    codigo_documento: Optional[str] = Field(None, min_length=3, max_length=50, description="Código del documento")
    id_vehiculo: int = Field(..., description="ID del conductor asociado")
    tipo_documento: str = Field(..., min_length=3, max_length=50, description="Tipo de documento del conductor")
    fecha_emision: Optional[datetime] = Field(None, description="Fecha de emisión del documento")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento del documento")
    esta_activo: Optional[bool] = Field(True, description="Indica si el documento está activo (soft delete)")

class DocumentoVehiculoCreate(DocumentoVehiculoBase):
    pass

class DocumentoVehiculoResponse(DocumentoVehiculoBase):
    id: int = Field(..., description="ID del documento del conductor")
    archivo_url: str = Field(..., min_length=5, max_length=255, description="URL del archivo del documento")
    archivo_nombre: str = Field(..., min_length=3, max_length=255, description="Nombre original del archivo del documento")
    fecha_creacion: datetime = Field(..., description="Fecha de carga del documento")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización del documento")

    class Config:
        from_attributes = True