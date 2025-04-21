from sqlalchemy.orm import Session
from datetime import datetime
from app.models.viaje_documentos import DocumentoViaje
from app.schemas.viajes_documentos_schemas import DocumentoViajeCreate

def crear_documento_viaje(db: Session, documento: DocumentoViajeCreate):
    db_documento = DocumentoViaje(**documento.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def obtener_documentos_viajes(db: Session):
    return db.query(DocumentoViaje).all()

def obtener_documento_viaje(db: Session, documento_id: int):
    return db.query(DocumentoViaje).filter(DocumentoViaje.id == documento_id).first()

def obtener_documentos_viaje_por_tipo(db: Session, tipo_documento: str):
    return db.query(DocumentoViaje).filter(DocumentoViaje.tipo_documento == tipo_documento).all()

def obtener_documentos_viaje_por_codigo(db: Session, codigo_documento: str):
    return db.query(DocumentoViaje).filter(DocumentoViaje.codigo_documento == codigo_documento).all()

def actualizar_documento_viaje(db: Session, documento_id: int, documento: DocumentoViajeCreate):
    db_documento = db.query(DocumentoViaje).filter(DocumentoViaje.id == documento_id).first()
    db_documento.codigo_documento = documento.codigo_documento
    db_documento.tipo_documento = documento.tipo_documento
    db_documento.archivo_url = documento.archivo_url
    db.commit()
    db.refresh(db_documento)
    return db_documento

def eliminar_documento_viaje(db: Session, documento_id: int):
    db_documento = db.query(DocumentoViaje).filter(DocumentoViaje.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento