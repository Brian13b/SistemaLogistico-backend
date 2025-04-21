from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.conductores_documentos_schemas import DocumentoConductorCreate
from app.models.conductor_documentos import ConductorDocumento

def crear_documento_conductor(db: Session, documento: DocumentoConductorCreate):
    db_documento = ConductorDocumento(**documento.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def obtener_documentos_conductores(db: Session):
    return db.query(ConductorDocumento).all()

def obtener_documento_conductor(db: Session, documento_id: int):
    return db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()

def obtener_documentos_por_tipo(db: Session, tipo_documento: str):
    return db.query(ConductorDocumento).filter(ConductorDocumento.tipo_documento == tipo_documento).all()

def obtener_documentos_vencidos(db: Session):
    hoy = datetime.now().date()
    return db.query(ConductorDocumento).filter(ConductorDocumento.fecha_vencimiento < hoy).all()

def actualizar_documento_conductor(db: Session, documento_id: int, documento: DocumentoConductorCreate):
    db_documento = db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()
    if db_documento is None:
        return None
    
    db_documento.tipo_documento = documento.tipo_documento
    db_documento.archivo_url = documento.archivo_url
    db_documento.fecha_vencimiento = documento.fecha_vencimiento
    db_documento.fecha_emision = documento.fecha_emision 
    db_documento.tamanio = documento.tamanio
    db_documento.actualizado_en = datetime.now()
    
    db.commit()
    db.refresh(db_documento)
    return db_documento

def eliminar_documento_conductor(db: Session, documento_id: int):
    db_documento = db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento

def obtener_documentos_del_conductor(db: Session, conductor_id: int):
    return db.query(ConductorDocumento).filter(ConductorDocumento.id_conductor == conductor_id).all()