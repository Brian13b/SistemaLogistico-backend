from sqlalchemy.orm import Session
from sqlalchemy import desc, extract, func
from app.models.gastos import Gasto
from app.schemas.gastos_schemas import GastoCreate
from fastapi import UploadFile
from typing import Optional, List
from datetime import date
from app.services.google_drive import drive_service

async def crear_gasto_con_archivo(db: Session, gasto: GastoCreate, archivo: Optional[UploadFile] = None):
    gasto_dict = gasto.model_dump()
    
    if archivo:
        try:
            file_info = await drive_service.upload_file_to_drive(archivo)
            
            gasto_dict["imagen_url"] = file_info.get('url') or file_info.get('webViewLink')
        except Exception as e:
            print(f"Advertencia: No se pudo subir el archivo a Drive: {e}")
            pass

    db_gasto = Gasto(**gasto_dict)
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
        
    return query.order_by(desc(Gasto.fecha)).offset(skip).limit(limit).all()

def obtener_resumen_gastos(db: Session, mes: int, anio: int):
    return db.query(
        Gasto.tipo_gasto, 
        func.sum(Gasto.monto).label("total")
    ).filter(
        extract('month', Gasto.fecha) == mes,
        extract('year', Gasto.fecha) == anio
    ).group_by(Gasto.tipo_gasto).all()