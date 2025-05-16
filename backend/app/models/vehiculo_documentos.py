from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class DocumentoVehiculo(Base):
    __tablename__ = "documentos_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    codigo_documento = Column(String, index=True)
    id_vehiculo = Column(Integer, ForeignKey('vehiculos.id', ondelete='CASCADE'))
    tipo_documento = Column(String, index=True)
    archivo_url = Column(String, index=True)
    archivo_nombre = Column(String, index=True)
    fecha_emision = Column(DateTime)
    fecha_vencimiento = Column(DateTime)
    esta_activo = Column(Boolean, default=True)
    archivo_drive_id = Column(String, index=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vehiculo = relationship("Vehiculo", back_populates="documentos")
