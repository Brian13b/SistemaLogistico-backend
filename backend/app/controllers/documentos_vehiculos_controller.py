import json
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.schemas.vehiculos_documentos_schemas import DocumentoVehiculoCreate, DocumentoVehiculoResponse
from app.crud.documentos_vehiculo_crud import (
    crear_documento_vehiculo_con_archivo,
    obtener_documentos_proximos_a_vencer,
    obtener_documentos_vehiculo_por_vehiculo,
    actualizar_documento_vehiculo_con_archivo, 
    eliminar_documento_vehiculo, 
    obtener_documentos_vehiculos, 
    obtener_documento_vehiculo,
    obtener_documentos_vehiculo_vencidos
) 
from app.database.database import get_db
from app.services.google_drive import drive_service

router = APIRouter()

@router.post("/documentos_vehiculos/", response_model=DocumentoVehiculoResponse)
async def crear_documento_vehiculo(documento_data: str = Form(...), archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """Crear un nuevo documento de vehículo con archivo."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoVehiculoCreate(**documento_dict)
        
        # Crear el documento con archivo
        return await crear_documento_vehiculo_con_archivo(db=db, documento=documento, archivo=archivo)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Error al procesar los datos JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/documentos_vehiculos/vehiculos/{vehiculo_id}", response_model=list[DocumentoVehiculoResponse])
def leer_documentos_vehiculo_por_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """Obtener documentos de vehículo por ID de vehículo."""
    db_documentos = obtener_documentos_vehiculo_por_vehiculo(db=db, vehiculo_id=vehiculo_id)
    if not db_documentos:
        raise HTTPException(status_code=404, detail="Documentos no encontrados")
    return db_documentos

@router.get("/documentos_vehiculos/", response_model=list[DocumentoVehiculoResponse])
def leer_documentos_vehiculos(db: Session = Depends(get_db)):
    """Obtener lista de documentos de vehículos."""
    return obtener_documentos_vehiculos(db=db)

@router.get("/documentos_vehiculos/{documento_vehiculo_id}", response_model=DocumentoVehiculoResponse)
def leer_documento_vehiculo(documento_vehiculo_id: int, db: Session = Depends(get_db)):
    """Obtener un documento de vehículo por ID."""
    documento_vehiculo = obtener_documento_vehiculo(db, documento_vehiculo_id)
    if documento_vehiculo is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    return documento_vehiculo

@router.put("/documentos_vehiculos/{documento_vehiculo_id}", response_model=DocumentoVehiculoResponse)
async def actualizar_documento_vehiculo(documento_vehiculo_id: int, documento_data: str = Form(...), archivo: Optional[UploadFile] = None, db: Session = Depends(get_db)):
    """Actualizar un documento de vehículo existente."""
    try:
        # Convertir string JSON a objeto Python
        documento_dict = json.loads(documento_data)
        documento = DocumentoVehiculoCreate(**documento_dict)

        db_documento = await actualizar_documento_vehiculo_con_archivo(db=db, documento_id=documento_vehiculo_id, documento=documento, archivo=archivo)

        if db_documento is None:
            raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
        return db_documento
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")

@router.delete("/documentos_vehiculos/{documento_vehiculo_id}")
def eliminar_documento_vehiculo_endpoint(documento_vehiculo_id: int, db: Session = Depends(get_db)):
    """Eliminar un documento de vehículo por ID."""
    documento_vehiculo_eliminado = eliminar_documento_vehiculo(db, documento_vehiculo_id)
    if documento_vehiculo_eliminado is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    return documento_vehiculo_eliminado

# Otras operaciones relacionadas con Documentos
@router.get("/documentos_vehiculos/vencidos/", response_model=list[DocumentoVehiculoResponse])
def leer_documentos_vehiculo_vencidos(db: Session = Depends(get_db)):
    """Obtener documentos de vehículos vencidos."""
    return obtener_documentos_vehiculo_vencidos(db=db)

@router.get("/documentos_vehiculos/proximos_vencimientos/{dias}", response_model=list[DocumentoVehiculoResponse])
def leer_documentos_vehiculo_proximos_vencimientos( dias: int = 30, db: Session = Depends(get_db)):
    """Obtener documentos de vehículos próximos a vencer."""
    return obtener_documentos_proximos_a_vencer(db=db, dias=dias)

@router.get("/documentos_vehiculos/{documento_vehiculo_id}/descargar")
async def descargar_documento_vehiculo(documento_vehiculo_id: int, db: Session = Depends(get_db)):
    """Descargar el archivo asociado a un documento de vehículo."""
    db_documento = obtener_documento_vehiculo(db=db, documento_id=documento_vehiculo_id)

    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    
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