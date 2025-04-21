import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.conductor_documentos import ConductorDocumento
from app.models.conductores import Conductor
from app.schemas.conductores_documentos_schemas import DocumentoConductor, DocumentoConductorCreate
from app.crud.documentos_conductor_crud import crear_documento_conductor, obtener_documento_conductor, obtener_documentos_conductores, actualizar_documento_conductor, eliminar_documento_conductor, obtener_documentos_por_tipo, obtener_documentos_vencidos, obtener_documentos_del_conductor
from app.database.database import get_db
from app.services.google_drive import GoogleDriveService

router = APIRouter()
drive_service = GoogleDriveService()

# Operaciones CRUD para Documentos
@router.post("/documentos_conductores/", response_model=DocumentoConductor)
async def guardar_documento_conductor(documento: DocumentoConductorCreate, db: Session = Depends(get_db)):

    drive_file = await drive_service.upload_file(documento.archivo_url, os.getenv("GOOGLE_DRIVE_FOLDER_ID"))
    
    return crear_documento_conductor(db=db, documento=documento)

@router.get("/documentos_conductores/", response_model=list[DocumentoConductor])
def leer_documentos_conductores(db: Session = Depends(get_db)):
    return obtener_documentos_conductores(db=db)

@router.get("/documentos_conductores/{documento_id}", response_model=DocumentoConductor)
def leer_documento_conductor(documento_id: int, db: Session = Depends(get_db)):
    db_documento = obtener_documento_conductor(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.put("/documentos_conductores/{documento_id}", response_model=DocumentoConductor)
def actualizar_documento_conductor(documento_id: int, documento: DocumentoConductorCreate, db: Session = Depends(get_db)):
    db_documento = actualizar_documento_conductor(db=db, documento_id=documento_id, documento=documento)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.delete("/documentos_conductores/{documento_id}", response_model=DocumentoConductor)
def eliminar_documento_conductor(documento_id: int, db: Session = Depends(get_db)):
    db_documento = eliminar_documento_conductor(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

# Otras operaciones relacionadas con Documentos
@router.get("/documentos_conductores/tipo/{tipo_documento}", response_model=list[DocumentoConductor])
def obtener_documentos_por_tipo(tipo_documento: str, db: Session = Depends(get_db)):
    return obtener_documentos_por_tipo(db=db, tipo_documento=tipo_documento)

@router.get("/documentos_conductores/vencidos/", response_model=list[DocumentoConductor])
def obtener_documentos_vencidos(db: Session = Depends(get_db)):
    return obtener_documentos_vencidos(db=db)

@router.get("/documentos_conductores/conductor/{conductor_id}", response_model=List[DocumentoConductor])
def obtener_documentos_por_conductor(conductor_id: int, db: Session = Depends(get_db)):
    conductor = db.query(Conductor).filter(Conductor.id == conductor_id).first()
    if not conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")

    documentos = db.query(ConductorDocumento).filter(ConductorDocumento.id_conductor == conductor_id).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este conductor")
    return documentos