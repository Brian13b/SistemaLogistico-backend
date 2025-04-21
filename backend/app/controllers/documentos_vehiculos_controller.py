from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.vehiculos_documentos_schemas import DocumentoVehiculo, DocumentoVehiculoCreate
from app.crud.documentos_vehiculo_crud import crear_documento_vehiculo, obtener_documento_vehiculo, obtener_documentos_vehiculos, actualizar_documento_vehiculo, eliminar_documento_vehiculo
from app.database.database import get_db

router = APIRouter()

@router.post("/documentos_vehiculos/", response_model=DocumentoVehiculo)
def crear_documento_vehiculo_api(documento_vehiculo: DocumentoVehiculoCreate, db: Session = Depends(get_db)):
    return crear_documento_vehiculo(db, documento_vehiculo)

@router.get("/documentos_vehiculos/", response_model=list[DocumentoVehiculo])
def obtener_documentos_vehiculos_api(db: Session = Depends(get_db)):
    return obtener_documentos_vehiculos(db)

@router.get("/documentos_vehiculos/{documento_vehiculo_id}", response_model=DocumentoVehiculo)
def obtener_documento_vehiculo_api(documento_vehiculo_id: int, db: Session = Depends(get_db)):
    documento_vehiculo = obtener_documento_vehiculo(db, documento_vehiculo_id)
    if documento_vehiculo is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    return documento_vehiculo

@router.put("/documentos_vehiculos/{documento_vehiculo_id}", response_model=DocumentoVehiculo)
def actualizar_documento_vehiculo_api(documento_vehiculo_id: int, documento_vehiculo: DocumentoVehiculoCreate, db: Session = Depends(get_db)):
    documento_vehiculo_actualizado = actualizar_documento_vehiculo(db, documento_vehiculo_id, documento_vehiculo)
    if documento_vehiculo_actualizado is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    return documento_vehiculo_actualizado

@router.delete("/documentos_vehiculos/{documento_vehiculo_id}")
def eliminar_documento_vehiculo_api(documento_vehiculo_id: int, db: Session = Depends(get_db)):
    documento_vehiculo_eliminado = eliminar_documento_vehiculo(db, documento_vehiculo_id)
    if documento_vehiculo_eliminado is None:
        raise HTTPException(status_code=404, detail="Documento vehiculo no encontrado")
    return {"mensaje": "Documento vehiculo eliminado"}
