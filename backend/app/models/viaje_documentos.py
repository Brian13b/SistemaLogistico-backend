from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class DocumentoViaje(Base):
    __tablename__ = "documentos_viajes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True)
    viaje_id = Column(Integer, ForeignKey("viajes.id"))
    tipo_documento = Column(String, index=True)
    codigo_documento = Column(String, index=True)
    fecha_emision = Column(DateTime)
    fecha_vencimiento = Column(DateTime)
    archivo_url = Column(String, index=True)
    archivo_nombre = Column(String, index=True)
    archivo_drive_id = Column(String, index=True)
    fecha_creacion = Column(DateTime, default=datetime.now)

    viaje = relationship("Viaje", back_populates="documentos")
