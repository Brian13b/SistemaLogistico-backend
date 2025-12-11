from sqlalchemy.orm import Session
from datetime import datetime
from app.models.vehiculos import Vehiculo
from app.schemas.vehiculos_schemas import VehiculoCreate

def crear_vehiculo(db: Session, vehiculo: VehiculoCreate):
    vehiculo_data = vehiculo.model_dump()

    if vehiculo_data.get('id_conductor') == 0:
        vehiculo_data['id_conductor'] = None

    db_vehiculo = Vehiculo(**vehiculo_data)
    
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def obtener_vehiculos(db: Session):
    return db.query(Vehiculo).all()

def obtener_vehiculo(db: Session, vehiculo_id: int):
    return db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

def buscar_vehiculos_por_marca(db: Session, marca: str):
    return db.query(Vehiculo).filter(Vehiculo.marca.ilike(f"%{marca}%")).all()

def buscar_vehiculos_por_modelo(db: Session, modelo: str):
    return db.query(Vehiculo).filter(Vehiculo.modelo.ilike(f"%{modelo}%")).all()

def obtener_vehiculos_por_estado(db: Session, estado: str):
    return db.query(Vehiculo).filter(Vehiculo.estado == estado).all()

def actualizar_vehiculo(db: Session, vehiculo_id: int, vehiculo: VehiculoCreate):
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not db_vehiculo:
        return None

    db_vehiculo.marca = vehiculo.marca
    db_vehiculo.modelo = vehiculo.modelo
    db_vehiculo.patente = vehiculo.patente
    db_vehiculo.anio = vehiculo.anio
    db_vehiculo.tipo = vehiculo.tipo
    db_vehiculo.estado = vehiculo.estado
    db_vehiculo.kilometraje = vehiculo.kilometraje
    
    if vehiculo.id_conductor == 0:
        db_vehiculo.id_conductor = None
    else:
        db_vehiculo.id_conductor = vehiculo.id_conductor

    db_vehiculo.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def eliminar_vehiculo(db: Session, vehiculo_id: int):
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    db.delete(db_vehiculo)
    db.commit()
    return db_vehiculo