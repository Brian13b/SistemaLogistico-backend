import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.schemas.conductores_documentos_schemas import DocumentoConductorCreate, DocumentoConductorResponse
from app.crud.documentos_conductor_crud import (
    crear_documento_conductor_con_archivo, 
    obtener_documentos_conductor_por_conductor,
    actualizar_documento_conductor_con_archivo,
    eliminar_documento_conductor,
    obtener_documentos_conductores,
    obtener_documento_conductor,
    obtener_documentos_proximos_a_vencer,
    obtener_documentos_vencidos
)
from app.database.database import get_db
from app.services.google_drive import drive_service

router = APIRouter()

@router.post("/documentos_conductores/", response_model=DocumentoConductorResponse)
async def guardar_documento_conductor(documento_data: str = Form(...), archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """Crear un nuevo documento de conductor con archivo."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoConductorCreate(**documento_dict)
        
        # Crear el documento con archivo
        return await crear_documento_conductor_con_archivo(db=db, documento=documento, archivo=archivo)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Error al procesar los datos JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/documentos_conductores/", response_model=list[DocumentoConductorResponse])
def leer_documentos_conductores(db: Session = Depends(get_db)):
    """Obtener lista de documentos de conductores."""
    return obtener_documentos_conductores(db=db)

@router.get("/documentos_conductores/conductor/{conductor_id}", response_model=list[DocumentoConductorResponse])
def leer_documentos_conductor_por_conductor(conductor_id: int, db: Session = Depends(get_db)):
    """Obtener documentos de conductor por ID de conductor."""
    db_documentos = obtener_documentos_conductor_por_conductor(db=db, conductor_id=conductor_id)
    if not db_documentos:
        raise HTTPException(status_code=404, detail="Documentos no encontrados")
    return db_documentos

@router.get("/documentos_conductores/{documento_id}", response_model=DocumentoConductorResponse)
def leer_documento_conductor(documento_id: int, db: Session = Depends(get_db)):
    """Obtener un documento de conductor por ID."""
    db_documento = obtener_documento_conductor(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.put("/documentos_conductores/{documento_id}", response_model=DocumentoConductorResponse)
async def actualizar_documento_conductor(documento_id: int, documento_data: str = Form(...), archivo: Optional[UploadFile] = None, db: Session = Depends(get_db)):
    """Actualizar un documento de conductor existente."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoConductorCreate(**documento_dict)

        db_documento = await actualizar_documento_conductor_con_archivo(db=db, documento_id=documento_id, documento=documento, archivo=archivo)

        if db_documento is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return db_documento
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.delete("/documentos_conductores/{documento_id}", response_model=DocumentoConductorResponse)
def eliminar_documento_conductor_endpoint(documento_id: int, db: Session = Depends(get_db)):
    db_documento = eliminar_documento_conductor(documento_id=documento_id, db=db)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

# Otras operaciones relacionadas con Documentos

@router.get("/documentos_conductores/vencidos/", response_model=list[DocumentoConductorResponse])
def leer_documentos_vencidos(db: Session = Depends(get_db)):
    """Obtener documentos de conductores vencidos."""
    return obtener_documentos_vencidos(db=db)

@router.get("/documentos_conductores/proximos_vencimientos/{dias}", response_model=list[DocumentoConductorResponse])
def leer_documentos_proximos_vencimientos(dias: int = 30, db: Session = Depends(get_db)):
    """Obtener documentos de conductores próximos a vencer."""
    return obtener_documentos_proximos_a_vencer(db=db, dias=dias)

@router.get("/documentos_conductores/{documento_id}/descargar")
async def descargar_documento_conductor(documento_id: int, db: Session = Depends(get_db)):
    """Descargar un documento de conductor por ID."""
    db_documento = obtener_documento_conductor(db=db, documento_id=documento_id)

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