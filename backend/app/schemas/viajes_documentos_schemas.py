from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DocumentoViajeBase(BaseModel):
    tipo_documento: str = Field(..., min_length=3, max_length=50, description="Tipo de documento del viaje")
    codigo_documento: Optional[str] = Field(None, min_length=3, max_length=50, description="Código del documento del viaje")
    fecha_emision: Optional[datetime] = Field(None, description="Fecha de emisión del documento")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento del documento")
    viaje_id: int = Field(..., description="ID del viaje asociado")

class DocumentoViajeCreate(DocumentoViajeBase):
    pass

class DocumentoViajeResponse(DocumentoViajeBase):
    id: int = Field(..., description="ID del documento del viaje")
    archivo_url: str = Field(..., description="URL del archivo del documento")
    archivo_nombre: str = Field(..., description="Nombre original del archivo")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del documento")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización del documento")
    
    class Config:
        from_attributes = True