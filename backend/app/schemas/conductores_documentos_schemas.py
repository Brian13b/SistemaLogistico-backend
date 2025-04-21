from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date

class DocumentoConductorBase(BaseModel):
    codigo: Optional[str] = Field(None, min_length=3, max_length=50, description="Código del documento")
    id_conductor: int = Field(..., description="ID del conductor asociado")
    tipo_documento: str = Field(..., min_length=3, max_length=50, description="Tipo de documento del conductor")
    nombre_original: Optional[str] = Field(..., min_length=3, max_length=255, description="Nombre original del archivo del documento")
    archivo_url: str = Field(..., min_length=5, max_length=255, description="URL del archivo del documento")
    tamanio: Optional[int] = Field(None, description="Tamaño en bytes del archivo")
    fecha_emision: Optional[date] = Field(None, description="Fecha de emisión del documento")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de vencimiento del documento")
    esta_activo: Optional[bool] = Field(True, description="Indica si el documento está activo (soft delete)")

class DocumentoConductorCreate(DocumentoConductorBase):
    pass

class DocumentoConductor(DocumentoConductorBase):
    id: int = Field(..., description="ID del documento del conductor")
    fecha_carga: datetime = Field(..., description="Fecha de carga del documento")
    actualizado_en: datetime = Field(..., description="Fecha de actualización del documento")

    class Config:
        from_attributes = True
