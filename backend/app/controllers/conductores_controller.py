from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.conductores_schemas import Conductor, ConductorCreate
from app.crud.conductores_crud import crear_conductor, obtener_conductores, obtener_conductor, actualizar_conductor, eliminar_conductor, buscar_conductores_por_nombre, buscar_conductores_por_apellido, obtener_conductores_con_licencias_proximas_a_vencer
from app.database.database import get_db

router = APIRouter()

@router.post("/conductores/")
def crear_conductor_endpoint(conductor: ConductorCreate, db: Session = Depends(get_db)):
    nuevo_conductor = crear_conductor(db, conductor)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Conductor creado exitosamente",
            "id": nuevo_conductor.id,
            "nombre": nuevo_conductor.nombre,
            "apellido": nuevo_conductor.apellido
        }
    )

@router.get("/conductores/", response_model=list[Conductor])
def leer_conductores(db: Session = Depends(get_db)):
    return obtener_conductores(db)

@router.get("/conductores/{conductor_id}", response_model=Conductor)
def leer_conductor(conductor_id: int, db: Session = Depends(get_db)):
    db_conductor = obtener_conductor(db, conductor_id)
    if db_conductor is None:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return db_conductor

@router.put("/conductores/{conductor_id}", response_model=Conductor)
def actualizar_conductor_endpoint(conductor_id: int, conductor: ConductorCreate, db: Session = Depends(get_db)):
    db_conductor = actualizar_conductor(db, conductor_id, conductor)
    if db_conductor is None:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return db_conductor

@router.delete("/conductores/{conductor_id}", response_model=Conductor)
def eliminar_conductor_endpoint(conductor_id: int, db: Session = Depends(get_db)):
    db_conductor = eliminar_conductor(db, conductor_id)
    if db_conductor is None:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return db_conductor

@router.get("/conductores/buscar/nombre/", response_model=list[Conductor])
def buscar_conductores_por_nombre_endpoint(nombre: str, db: Session = Depends(get_db)):
    return buscar_conductores_por_nombre(db, nombre)

@router.get("/conductores/buscar/apellido/", response_model=list[Conductor])
def buscar_conductores_por_apellido_endpoint(apellido: str, db: Session = Depends(get_db)):
    return buscar_conductores_por_apellido(db, apellido)

@router.get("/conductores/licencias_proximas_a_vencer/", response_model=list[Conductor])
def obtener_conductores_con_licencias_proximas_a_vencer_endpoint(dias_antes: int, db: Session = Depends(get_db)):
    return obtener_conductores_con_licencias_proximas_a_vencer(db, dias_antes)