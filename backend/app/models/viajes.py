from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class Viaje(Base):
    __tablename__ = 'viajes'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True)
    origen = Column(String)
    destino = Column(String)
    vehiculo_id = Column(Integer, ForeignKey('vehiculos.id'))
    conductor_id = Column(Integer, ForeignKey('conductores.id'))
    fecha_salida = Column(Date)
    fecha_llegada = Column(Date)
    producto = Column(String)
    precio = Column(Float)
    peso = Column(Float)
    unidad_medida = Column(String)
    estado = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vehiculo = relationship('Vehiculo', back_populates='viajes')
    conductor = relationship('Conductor', back_populates='viajes')
    documentos = relationship('DocumentoViaje', back_populates='viaje')