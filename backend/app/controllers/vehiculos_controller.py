from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.vehiculos_schemas import Vehiculo, VehiculoCreate, VehiculoLigero
from app.crud.vehiculos_crud import crear_vehiculo, obtener_vehiculos, obtener_vehiculo, actualizar_vehiculo, eliminar_vehiculo, buscar_vehiculos_por_marca, buscar_vehiculos_por_modelo, obtener_vehiculos_por_estado

router = APIRouter()

@router.post("/vehiculos/")
def crear_vehiculo_endpoint(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo_vehiculo = crear_vehiculo(db, vehiculo)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Vehículo creado exitosamente",
            "id": nuevo_vehiculo.id,
            "marca": nuevo_vehiculo.marca,
            "modelo": nuevo_vehiculo.modelo
        }
    )

@router.get("/vehiculos/", response_model=list[VehiculoLigero])
def leer_vehiculos(db: Session = Depends(get_db)):
    return obtener_vehiculos(db)

@router.get("/vehiculos/{vehiculo_id}", response_model=Vehiculo)
def leer_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    db_vehiculo = obtener_vehiculo(db, vehiculo_id)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

@router.put("/vehiculos/{vehiculo_id}", response_model=Vehiculo)
def actualizar_vehiculo_endpoint(vehiculo_id: int, vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    db_vehiculo = actualizar_vehiculo(db, vehiculo_id, vehiculo)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

@router.delete("/vehiculos/{vehiculo_id}", response_model=Vehiculo)
def eliminar_vehiculo_endpoint(vehiculo_id: int, db: Session = Depends(get_db)):
    db_vehiculo = eliminar_vehiculo(db, vehiculo_id)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

@router.get("/vehiculos/buscar/marca/", response_model=list[Vehiculo])
def buscar_vehiculos_por_marca_endpoint(marca: str, db: Session = Depends(get_db)):
    return buscar_vehiculos_por_marca(db, marca)

@router.get("/vehiculos/buscar/modelo/", response_model=list[Vehiculo])
def buscar_vehiculos_por_modelo_endpoint(modelo: str, db: Session = Depends(get_db)):
    return buscar_vehiculos_por_modelo(db, modelo)

@router.get("/vehiculos/estado/{estado}", response_model=list[Vehiculo])
def obtener_vehiculos_por_estado_endpoint(estado: str, db: Session = Depends(get_db)):
    return obtener_vehiculos_por_estado(db, estado)