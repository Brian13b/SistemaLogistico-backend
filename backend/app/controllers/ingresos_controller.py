from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.ingresos_schemas import Ingreso, IngresoCreate
from app.crud.ingresos_crud import crear_ingreso, obtener_ingresos, obtener_ingreso, eliminar_ingreso, obtener_ingresos_por_viaje, actualizar_ingreso

router = APIRouter()

@router.post("/ingresos/")
def crear_ingreso_endpoint(ingreso: IngresoCreate, db: Session = Depends(get_db)):
    nuevo_ingreso = crear_ingreso(db, ingreso)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Ingreso creado exitosamente",
            "id": nuevo_ingreso.id,
            "monto": nuevo_ingreso.monto
        }
    )

@router.get("/ingresos/", response_model=list[Ingreso])
def obtener_ingresos_endpoint(db: Session = Depends(get_db)):
    return obtener_ingresos(db)

@router.get("/ingresos/{ingreso_id}", response_model=Ingreso)
def obtener_ingreso_endpoint(ingreso_id: int, db: Session = Depends(get_db)):
    ingreso = obtener_ingreso(db, ingreso_id)
    if not ingreso:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return ingreso

@router.get("/ingresos/viaje/{viaje_id}", response_model=list[Ingreso])
def obtener_ingresos_por_viaje_endpoint(viaje_id: int, db: Session = Depends(get_db)):
    return obtener_ingresos_por_viaje(db, viaje_id=viaje_id)

@router.put("/ingresos/{ingreso_id}", response_model=Ingreso)
def actualizar_ingreso_endpoint(ingreso_id: int, ingreso: IngresoCreate, db: Session = Depends(get_db)):
    return actualizar_ingreso(db, ingreso_id, ingreso)

@router.delete("/ingresos/{ingreso_id}", response_model=Ingreso)
def eliminar_ingreso_endpoint(ingreso_id: int, db: Session = Depends(get_db)):
    ingreso = eliminar_ingreso(db, ingreso_id)
    if not ingreso:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return ingreso