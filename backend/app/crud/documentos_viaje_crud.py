from sqlalchemy.orm import Session
from datetime import datetime
from app.models.viaje_documentos import DocumentoViaje
from app.schemas.viajes_documentos_schemas import DocumentoViajeCreate
from app.services.google_drive import drive_service

async def crear_documento_viaje_con_archivo(db: Session, documento: DocumentoViajeCreate, archivo):
    """Crear un documento de viaje con su archivo asociado."""
    # Subir archivo a Google Drive
    file_info = await drive_service.upload_file_to_drive(archivo)
    
    # Crear instancia del modelo con los datos del documento y archivo
    db_documento = DocumentoViaje(
        codigo=documento.codigo,
        tipo_documento=documento.tipo_documento,
        codigo_documento=documento.codigo_documento,
        fecha_emision=documento.fecha_emision,
        fecha_vencimiento=documento.fecha_vencimiento,
        viaje_id=documento.viaje_id,
        archivo_url=file_info['url'],
        archivo_nombre=archivo.filename,
        archivo_drive_id=file_info['drive_id']
    )
    
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

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

def obtener_documentos_viaje_por_viaje(db: Session, viaje_id: int):
    return db.query(DocumentoViaje).filter(DocumentoViaje.viaje_id == viaje_id).all()

async def actualizar_documento_viaje_con_archivo(db: Session, documento_id: int, documento: DocumentoViajeCreate, archivo=None):
    """Actualizar un documento de viaje y opcionalmente su archivo."""
    db_documento = db.query(DocumentoViaje).filter(DocumentoViaje.id == documento_id).first()
    
    if not db_documento:
        return None
    
    # Actualizar campos básicos
    for key, value in documento.model_dump().items():
        setattr(db_documento, key, value)
    
    # Si se proporciona un nuevo archivo, subirlo y actualizar referencias
    if archivo:
        file_info = await drive_service.upload_file_to_drive(
            archivo.file, 
            archivo.filename, 
            archivo.content_type
        )
        
        db_documento.archivo_url = file_info['url']
        db_documento.archivo_nombre = archivo.filename
        db_documento.archivo_drive_id = file_info['drive_id']
    
    db.commit()
    db.refresh(db_documento)
    return db_documento

def eliminar_documento_viaje(db: Session, documento_id: int):
    db_documento = db.query(DocumentoViaje).filter(DocumentoViaje.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento