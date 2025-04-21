from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.viajes_documentos_schemas import DocumentoViaje, DocumentoViajeCreate
from app.crud.documentos_viaje_crud import crear_documento_viaje, obtener_documento_viaje, obtener_documentos_viajes, actualizar_documento_viaje, eliminar_documento_viaje
from app.database.database import get_db

router = APIRouter()

@router.post("/documentos_viajes/", response_model=DocumentoViaje)
def crear_documento_viaje_endpoint(documento: DocumentoViajeCreate, db: Session = Depends(get_db)):
    return crear_documento_viaje(db=db, documento=documento)

@router.get("/documentos_viajes/", response_model=list[DocumentoViaje])
def leer_documentos_viajes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_documentos_viajes(db=db, skip=skip, limit=limit)

@router.get("/documentos_viajes/{documento_id}", response_model=DocumentoViaje)
def leer_documento_viaje(documento_id: int, db: Session = Depends(get_db)):
    db_documento = obtener_documento_viaje(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.put("/documentos_viajes/{documento_id}", response_model=DocumentoViaje)
def actualizar_documento_viaje_endpoint(documento_id: int, documento: DocumentoViajeCreate, db: Session = Depends(get_db)):
    db_documento = actualizar_documento_viaje(db=db, documento_id=documento_id, documento=documento)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento

@router.delete("/documentos_viajes/{documento_id}", response_model=DocumentoViaje)
def eliminar_documento_viaje_endpoint(documento_id: int, db: Session = Depends(get_db)):
    db_documento = eliminar_documento_viaje(db=db, documento_id=documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return db_documento