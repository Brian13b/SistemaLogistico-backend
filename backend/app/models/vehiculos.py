from sqlalchemy import Column, Double, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    patente = Column(String, unique=True, index=True)
    anio = Column(Integer)
    tipo = Column(String)
    tara = Column(Integer)
    carga_maxima = Column(Integer)
    estado = Column(String)
    fecha_alta = Column(DateTime, default=datetime.now)
    fecha_baja = Column(DateTime, nullable=True)
    fecha_actualizacion = Column(DateTime, default=datetime.now)
    kilometraje = Column(Double)
    id_conductor = Column(Integer, ForeignKey("conductores.id"))

    conductor = relationship("Conductor", back_populates="vehiculos")
    viajes = relationship("Viaje", back_populates="vehiculo")
    documentos = relationship("DocumentoVehiculo", back_populates="vehiculo")
    gastos = relationship("Gasto", back_populates="vehiculo")
