from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.conductor_documentos import ConductorDocumento
from app.schemas.conductores_documentos_schemas import DocumentoConductorCreate
from app.services.google_drive import drive_service

async def crear_documento_conductor_con_archivo(db: Session, documento: DocumentoConductorCreate, archivo):
    file_info = await drive_service.upload_file_to_drive(archivo)
    
    db_documento = ConductorDocumento(
        tipo_documento=documento.tipo_documento,
        codigo_documento=documento.codigo_documento,
        fecha_emision=documento.fecha_emision,
        fecha_vencimiento=documento.fecha_vencimiento,
        id_conductor=documento.id_conductor,
        esta_activo=documento.esta_activo,
        archivo_url=file_info['url'],
        archivo_nombre=archivo.filename,
        archivo_drive_id=file_info['drive_id']
    )
    
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def obtener_documentos_conductor_por_conductor(db: Session, conductor_id: int):
    return db.query(ConductorDocumento).filter(ConductorDocumento.id_conductor == conductor_id).all()

async def actualizar_documento_conductor_con_archivo(db: Session, documento_id: int, documento: DocumentoConductorCreate, archivo=None):
    db_documento = db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()
    
    if not db_documento:
        return None
    
    for key, value in documento.model_dump().items():
        setattr(db_documento, key, value)
    
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

def eliminar_documento_conductor(db: Session, documento_id: int):
    db_documento = db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento

# Otros métodos de consulta
def obtener_documentos_conductores(db: Session):
    return db.query(ConductorDocumento).all()

def obtener_documento_conductor(db: Session, documento_id: int):
    return db.query(ConductorDocumento).filter(ConductorDocumento.id == documento_id).first()

def obtener_documentos_por_tipo(db: Session, tipo_documento: str):
    return db.query(ConductorDocumento).filter(ConductorDocumento.tipo_documento == tipo_documento).all()

def obtener_documentos_vencidos(db: Session):
    hoy = datetime.now().date()
    return db.query(ConductorDocumento).filter(ConductorDocumento.fecha_vencimiento < hoy).all()

def obtener_documentos_proximos_a_vencer(db: Session, dias: int = 30):
    hoy = datetime.now().date()
    fecha_limite = hoy + timedelta(days=dias)
    return db.query(ConductorDocumento).filter(
        ConductorDocumento.fecha_vencimiento >= hoy,
        ConductorDocumento.fecha_vencimiento <= fecha_limite
    ).all()
