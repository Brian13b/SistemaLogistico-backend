from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.models.gasto import Gasto
from app.schemas.gasto import GastoCreate, GastoUpdate
from datetime import date
from typing import Optional

def crear_gasto(db: Session, gasto: GastoCreate):
    db_gasto = Gasto(**gasto.dict())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

def obtener_gastos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    vehiculo_id: Optional[int] = None
):
    query = db.query(Gasto)
    
    if fecha_desde:
        query = query.filter(Gasto.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Gasto.fecha <= fecha_hasta)
    if vehiculo_id:
        query = query.filter(Gasto.vehiculo_id == vehiculo_id)
        
    return query.order_by(Gasto.fecha.desc()).offset(skip).limit(limit).all()

def obtener_resumen_gastos(db: Session, mes: int, anio: int):
    """Calcula el total de gastos del mes agrupado por tipo"""
    return db.query(
        Gasto.tipo_gasto, 
        func.sum(Gasto.monto).label("total")
    ).filter(
        extract('month', Gasto.fecha) == mes,
        extract('year', Gasto.fecha) == anio
    ).group_by(Gasto.tipo_gasto).all()