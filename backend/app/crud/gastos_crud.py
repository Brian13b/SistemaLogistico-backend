from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.gastos import Gasto
from app.schemas.gastos_schemas import GastoCreate

def crear_gasto(db: Session, gasto: GastoCreate):
    db_gasto = Gasto(**gasto.model_dump())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

def obtener_gasto(db: Session, gasto_id: int):
    return db.query(Gasto).filter(Gasto.id == gasto_id).first()

def obtener_gastos(db: Session):
    return db.query(Gasto).all()

def obtener_gastos_por_viaje(db: Session, viaje_id: int):
    return db.query(Gasto).filter(Gasto.viaje_id == viaje_id).all()

def eliminar_gasto(db: Session, gasto_id: int):
    db_gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    db.delete(db_gasto)
    db.commit()
    return db_gasto

def exportar_gastos(db: Session, viaje_id: int = None, cantidad: int = None, rango: str = None):
    query = db.query(Gasto)
    if viaje_id:
        query = query.filter(Gasto.viaje_id == viaje_id)
    if rango:
        hoy = datetime.today().date()
        if rango == "10dias":
            fecha_inicio = hoy - timedelta(days=10)
        elif rango == "mes":
            fecha_inicio = hoy - timedelta(days=30)
        elif rango == "6meses":
            fecha_inicio = hoy - timedelta(days=180)
        else:
            fecha_inicio = None
        if fecha_inicio:
            query = query.filter(Gasto.fecha >= fecha_inicio)
    if cantidad:
        query = query.order_by(Gasto.fecha.desc()).limit(cantidad)
    return query.all()