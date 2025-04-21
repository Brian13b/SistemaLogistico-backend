from sqlalchemy.orm import Session
from datetime import datetime
from app.models.vehiculo_documentos import DocumentoVehiculo
from app.schemas.vehiculos_documentos_schemas import DocumentoVehiculoCreate

def crear_documento_vehiculo(db: Session, documento: DocumentoVehiculoCreate):
    db_documento = DocumentoVehiculo(**documento.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def obtener_documentos_vehiculos(db: Session):
    return db.query(DocumentoVehiculo).all()

def obtener_documento_vehiculo(db: Session, documento_id: int):
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()

def obtener_documentos_vehiculo_por_tipo(db: Session, tipo_documento: str):
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.tipo_documento == tipo_documento).all()

def obtener_documentos_vehiculo_vencidos(db: Session):
    hoy = datetime.now().date()
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.fecha_vencimiento < hoy).all()

def actualizar_documento_vehiculo(db: Session, documento_id: int, documento: DocumentoVehiculoCreate):
    db_documento = db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()
    db_documento.tipo_documento = documento.tipo_documento
    db_documento.numero_documento = documento.numero_documento
    db_documento.fecha_emision = documento.fecha_emision
    db_documento.fecha_vencimiento = documento.fecha_vencimiento
    db_documento.archivo_url = documento.archivo_url
    db_documento.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(db_documento)
    return db_documento

def eliminar_documento_vehiculo(db: Session, documento_id: int):
    db_documento = db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento