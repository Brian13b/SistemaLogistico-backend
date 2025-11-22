from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.models.ingreso import Ingreso
from app.schemas.ingreso import IngresoCreate
from datetime import date
from typing import Optional

def crear_ingreso(db: Session, ingreso: IngresoCreate):
    db_ingreso = Ingreso(**ingreso.dict())
    db.add(db_ingreso)
    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso

def obtener_ingresos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    fecha_desde: Optional[date] = None
):
    query = db.query(Ingreso)
    if fecha_desde:
        query = query.filter(Ingreso.fecha >= fecha_desde)
    return query.order_by(Ingreso.fecha.desc()).offset(skip).limit(limit).all()

def obtener_resumen_ingresos(db: Session, mes: int, anio: int):
    return db.query(
        func.sum(Ingreso.monto).label("total")
    ).filter(
        extract('month', Ingreso.fecha) == mes,
        extract('year', Ingreso.fecha) == anio
    ).scalar() or 0.0
