from sqlalchemy.orm import Session
from sqlalchemy import desc, extract, func
from app.models.ingresos import Ingreso
from app.schemas.ingresos_schemas import IngresoCreate
from fastapi import UploadFile
from typing import Optional
from datetime import date
from app.services.google_drive import drive_service

async def crear_ingreso_con_archivo(db: Session, ingreso: IngresoCreate, archivo: Optional[UploadFile] = None):
    ingreso_dict = ingreso.model_dump()
    
    if archivo:
        try:
            # Reutilizamos el servicio de Drive
            file_info = await drive_service.upload_file_to_drive(archivo)
            ingreso_dict["imagen_url"] = file_info.get('url') or file_info.get('webViewLink')
        except Exception as e:
            print(f"Advertencia: Error subiendo a Drive (Ingresos): {e}")
            pass

    db_ingreso = Ingreso(**ingreso_dict)
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
    return query.order_by(desc(Ingreso.fecha)).offset(skip).limit(limit).all()

def obtener_resumen_ingresos(db: Session, mes: int, anio: int):
    return db.query(func.sum(Ingreso.monto).label("total")).filter(
        extract('month', Ingreso.fecha) == mes,
        extract('year', Ingreso.fecha) == anio
    ).scalar() or 0.0