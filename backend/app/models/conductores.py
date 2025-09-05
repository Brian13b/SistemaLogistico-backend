from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class Conductor(Base):
    __tablename__ = 'conductores'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    foto = Column(String)
    dni = Column(String, nullable=False, unique=True)
    numero_contacto = Column(String)
    email_contacto = Column(String(50))
    direccion = Column(String(100), nullable=False)
    estado = Column(String(10), nullable=False, default='Activo')
    creado_en = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vehiculos = relationship("Vehiculo", back_populates="conductor")
    viajes = relationship("Viaje", back_populates="conductor")
    documentos = relationship("ConductorDocumento", back_populates="conductor")