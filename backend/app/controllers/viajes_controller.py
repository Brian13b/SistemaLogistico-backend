from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.viajes_schemas import Viaje, ViajeCreate
from app.crud.viajes_crud import crear_viaje, obtener_viajes, obtener_viaje, actualizar_viaje, eliminar_viaje, buscar_viajes_por_origen, buscar_viajes_por_destino, obtener_viajes_por_estado, obtener_viajes_por_rango_fechas
from app.database.database import get_db

router = APIRouter()

@router.post("/viajes/", response_model=Viaje)
def crear_viaje_endpoint(viaje: ViajeCreate, db: Session = Depends(get_db)):
    return crear_viaje(db, viaje)

@router.get("/viajes/", response_model=list[Viaje])
def leer_viajes(db: Session = Depends(get_db)):
    return obtener_viajes(db)

@router.get("/viajes/{viaje_id}", response_model=Viaje)
def leer_viaje(viaje_id: int, db: Session = Depends(get_db)):
    db_viaje = obtener_viaje(db, viaje_id)
    if db_viaje is None:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return db_viaje

@router.put("/viajes/{viaje_id}", response_model=Viaje)
def actualizar_viaje_endpoint(viaje_id: int, viaje: ViajeCreate, db: Session = Depends(get_db)):
    db_viaje = actualizar_viaje(db, viaje_id, viaje)
    if db_viaje is None:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return db_viaje

@router.delete("/viajes/{viaje_id}", response_model=Viaje)
def eliminar_viaje_endpoint(viaje_id: int, db: Session = Depends(get_db)):
    db_viaje = eliminar_viaje(db, viaje_id)
    if db_viaje is None:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return db_viaje

@router.get("/viajes/buscar/origen/", response_model=list[Viaje])
def buscar_viajes_por_origen_endpoint(origen: str, db: Session = Depends(get_db)):
    return buscar_viajes_por_origen(db, origen)

@router.get("/viajes/buscar/destino/", response_model=list[Viaje])
def buscar_viajes_por_destino_endpoint(destino: str, db: Session = Depends(get_db)):
    return buscar_viajes_por_destino(db, destino)

@router.get("/viajes/estado/{estado}", response_model=list[Viaje])
def obtener_viajes_por_estado_endpoint(estado: str, db: Session = Depends(get_db)):
    return obtener_viajes_por_estado(db, estado)

@router.get("/viajes/rango_fechas/", response_model=list[Viaje])
def obtener_viajes_por_rango_fechas_endpoint(fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    return obtener_viajes_por_rango_fechas(db, fecha_inicio, fecha_fin)