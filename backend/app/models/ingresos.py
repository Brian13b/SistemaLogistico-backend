from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database.database import Base

class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_ingreso = Column(String, nullable=False, default='VIAJE') 

    viaje_id = Column(Integer, ForeignKey("viajes.id"), nullable=True)
    
    cliente_cuit = Column(String, nullable=True) 
    
    descripcion = Column(String, nullable=True)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    imagen_url = Column(String, nullable=True)

    creado_en = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    viaje = relationship("Viaje", back_populates="ingresos")
