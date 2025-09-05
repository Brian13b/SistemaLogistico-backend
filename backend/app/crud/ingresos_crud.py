from sqlalchemy.orm import Session
from app.models.ingresos import Ingreso
from app.schemas.ingresos_schemas import IngresoCreate

def crear_ingreso(db: Session, ingreso: IngresoCreate):
    db_ingreso = Ingreso(**ingreso.model_dump())
    db.add(db_ingreso)
    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso

def obtener_ingreso(db: Session, ingreso_id: int):
    return db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()

def obtener_ingresos(db: Session):
    return db.query(Ingreso).all()

def obtener_ingresos_por_viaje(db: Session, viaje_id: int):
    return db.query(Ingreso).filter(Ingreso.viaje_id == viaje_id).all()

def actualizar_ingreso(db: Session, ingreso_id: int, ingreso: IngresoCreate):
    db_ingreso = db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
    db_ingreso.descripcion = ingreso.descripcion
    db_ingreso.monto = ingreso.monto
    db_ingreso.fecha = ingreso.fecha
    db_ingreso.imagen_url = ingreso.imagen_url
    db_ingreso.viaje_id = ingreso.viaje_id
    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso

def eliminar_ingreso(db: Session, ingreso_id: int):
    db_gasto = db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
    db.delete(db_gasto)
    db.commit()
    return db_gasto
