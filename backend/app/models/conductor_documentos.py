from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class ConductorDocumento(Base):
    __tablename__ = 'documentos_conductores'
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True)
    id_conductor = Column(Integer, ForeignKey('conductores.id', ondelete='CASCADE'))
    tipo_documento = Column(String(50), nullable=False)
    nombre_original = Column(String(255), nullable=False)  # Nombre original del archivo
    archivo_url = Column(String(255), nullable=False)  # UUID generado + extensión
    tamanio = Column(Integer)  # Tamaño en bytes
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    esta_activo = Column(Boolean, default=True)  # Para soft delete
    fecha_carga = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    conductor = relationship('Conductor', back_populates='documentos')