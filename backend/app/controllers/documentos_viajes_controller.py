from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.schemas.viajes_documentos_schemas import DocumentoViajeResponse, DocumentoViajeCreate
from app.crud.documentos_viaje_crud import (
    crear_documento_viaje_con_archivo, 
    obtener_documento_viaje,
    obtener_documentos_viaje_por_viaje, 
    obtener_documentos_viajes, 
    actualizar_documento_viaje_con_archivo, 
    eliminar_documento_viaje
)
from app.database.database import get_db
from app.services.google_drive import drive_service

router = APIRouter()

@router.post("/documentos_viajes/", response_model=DocumentoViajeResponse)
async def crear_documento_viaje(documento_data: str = Form(...), archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """Crear un nuevo documento de viaje con archivo."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoViajeCreate(**documento_dict)
        
        # Crear el documento con archivo
        return await crear_documento_viaje_con_archivo(db=db, documento=documento, archivo=archivo)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Error al procesar los datos JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/documentos_viajes/", response_model=list[DocumentoViajeResponse])
def leer_documentos_viajes(db: Session = Depends(get_db)):
    """Obtener lista de documentos de viaje."""
    return obtener_documentos_viajes(db=db)

@router.get("/documentos_viajes/viajes/{viaje_id}", response_model=list[DocumentoViajeResponse])
def leer_documentos_viaje_por_viaje(viaje_id: int, db: Session = Depends(get_db)):
    """Obtener documentos de viaje por ID de viaje."""
    db_documentos = obtener_documentos_viaje_por_viaje(db=db, viaje_id=viaje_id)
    if not db_documentos:
        raise HTTPException(status_code=404, detail="Documentos no encontrados")
    return db_documentos

@router.get("/documentos_viajes/{documento_id}", response_model=DocumentoViajeResponse)
def leer_documento_viaje(documento_id: int, db: Session = Depends(get_db)):
    """Obtener un documento de viaje por ID."""
    db_documento = obtener_documento_viaje(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.put("/documentos_viajes/{documento_id}", response_model=DocumentoViajeResponse)
async def actualizar_documento_viaje(documento_id: int, documento_data: str = Form(...), archivo: Optional[UploadFile] = None, db: Session = Depends(get_db)):
    """Actualizar un documento de viaje existente."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoViajeCreate(**documento_dict)
        
        db_documento = await actualizar_documento_viaje_con_archivo(
            db=db, 
            documento_id=documento_id, 
            documento=documento, 
            archivo=archivo
        )
        
        if db_documento is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return db_documento
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.delete("/documentos_viajes/{documento_id}", response_model=DocumentoViajeResponse)
def eliminar_documento_viaje_endpoint(documento_id: int, db: Session = Depends(get_db)):
    """Eliminar un documento de viaje."""
    db_documento = eliminar_documento_viaje(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.get("/documentos_viajes/{documento_id}/descargar")
async def descargar_documento_viaje(documento_id: int, db: Session = Depends(get_db)):
    """Descargar el archivo asociado a un documento de viaje."""
    db_documento = obtener_documento_viaje(db=db, documento_id=documento_id)

    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    try:
        archivo_content = await drive_service.download_file_from_drive(db_documento.archivo_drive_id)
        
        return StreamingResponse(
            archivo_content,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={db_documento.archivo_nombre}"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el archivo: {str(e)}")