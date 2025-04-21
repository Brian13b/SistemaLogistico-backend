from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class DocumentoVehiculo(Base):
    __tablename__ = "documentos_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True)
    id_vehiculo = Column(Integer, ForeignKey('vehiculos.id', ondelete='CASCADE'))
    tipo_documento = Column(String(50), nullable=False)
    nombre_original = Column(String(255), nullable=False)  # Nombre original del archivo
    archivo_url = Column(String(255), nullable=False)  # UUID generado + extensión
    tamanio = Column(Integer)  # Tamaño en bytes
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    esta_activo = Column(Boolean, default=True)  # Para soft delete
    fecha_carga = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vehiculo = relationship("Vehiculo", back_populates="documentos")
