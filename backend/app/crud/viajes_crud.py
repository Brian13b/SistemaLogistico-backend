from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models.viajes import Viaje
from app.schemas.viajes_schemas import ViajeCreate

def crear_viaje(db: Session, viaje: ViajeCreate):
    db_viaje = Viaje(**viaje.model_dump())
    db.add(db_viaje)
    db.commit()
    db.refresh(db_viaje)
    return db_viaje

def obtener_viajes(db: Session):
    return db.query(Viaje).order_by(Viaje.fecha_salida.desc()).all()


def obtener_viaje(db: Session, viaje_id: int):
    return db.query(Viaje).filter(Viaje.id == viaje_id).first()

def buscar_viajes_por_origen(db: Session, origen: str):
    return db.query(Viaje).filter(Viaje.origen.ilike(f"%{origen}%")).all()

def buscar_viajes_por_destino(db: Session, destino: str):
    return db.query(Viaje).filter(Viaje.destino.ilike(f"%{destino}%")).all()

def obtener_viajes_por_estado(db: Session, estado: str):
    return db.query(Viaje).filter(Viaje.estado == estado).all()

def obtener_viajes_por_rango_fechas(db: Session, fecha_inicio: date, fecha_fin: date):
    return db.query(Viaje).filter(Viaje.fecha_salida >= fecha_inicio, Viaje.fecha_llegada <= fecha_fin).all()

def actualizar_viaje(db: Session, viaje_id: int, viaje: ViajeCreate):
    db_viaje = db.query(Viaje).filter(Viaje.id == viaje_id).first()
    db_viaje.origen = viaje.origen
    db_viaje.destino = viaje.destino
    db_viaje.vehiculo_id = viaje.vehiculo_id
    db_viaje.fecha_salida = viaje.fecha_salida
    db_viaje.fecha_llegada = viaje.fecha_llegada
    db_viaje.precio = viaje.precio
    db_viaje.peso = viaje.peso
    db_viaje.estado = viaje.estado
    db_viaje.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(db_viaje)
    return db_viaje

def eliminar_viaje(db: Session, viaje_id: int):
    db_viaje = db.query(Viaje).filter(Viaje.id == viaje_id).first()
    db.delete(db_viaje)
    db.commit()
    return db_viaje