from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.vehiculo_documentos import DocumentoVehiculo
from app.schemas.vehiculos_documentos_schemas import DocumentoVehiculoCreate
from app.services.google_drive import drive_service

# Create
async def crear_documento_vehiculo_con_archivo(db: Session, documento: DocumentoVehiculoCreate, archivo):
    """Crear un documento de vehículo con su archivo asociado."""
    file_info = await drive_service.upload_file_to_drive(archivo)
    
    db_documento = DocumentoVehiculo(
        tipo_documento=documento.tipo_documento,
        codigo_documento=documento.codigo_documento,
        fecha_emision=documento.fecha_emision,
        fecha_vencimiento=documento.fecha_vencimiento,
        id_vehiculo=documento.id_vehiculo,
        esta_activo=documento.esta_activo,
        archivo_url=file_info['url'],
        archivo_nombre=archivo.filename,
        archivo_drive_id=file_info['drive_id']
    )
    
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

# Read
def obtener_documentos_vehiculo_por_vehiculo(db: Session, vehiculo_id: int):
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id_vehiculo == vehiculo_id).all()

# Update
async def actualizar_documento_vehiculo_con_archivo(db: Session, documento_id: int, documento: DocumentoVehiculoCreate, archivo=None):
    """Actualizar un documento de vehículo y opcionalmente su archivo."""
    db_documento = db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()
    
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

# Delete
def eliminar_documento_vehiculo(db: Session, documento_id: int):
    db_documento = db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()
    db.delete(db_documento)
    db.commit()
    return db_documento

# Otros métodos adicionales
def obtener_documentos_vehiculos(db: Session):
    return db.query(DocumentoVehiculo).all()

def obtener_documento_vehiculo(db: Session, documento_id: int):
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.id == documento_id).first()

def obtener_documentos_vehiculo_por_tipo(db: Session, tipo_documento: str):
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.tipo_documento == tipo_documento).all()

def obtener_documentos_vehiculo_vencidos(db: Session):
    hoy = datetime.now().date()
    return db.query(DocumentoVehiculo).filter(DocumentoVehiculo.fecha_vencimiento < hoy).all()

def obtener_documentos_proximos_a_vencer(db: Session, dias: int = 30):
    hoy = datetime.now().date()
    fecha_limite = hoy + timedelta(days=dias)
    return db.query(DocumentoVehiculo).filter(
        DocumentoVehiculo.fecha_vencimiento >= hoy,
        DocumentoVehiculo.fecha_vencimiento <= fecha_limite
    ).all()