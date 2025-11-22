from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.ingreso import IngresoCreate, IngresoResponse
from app.crud import ingresos_crud

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])

@router.post("/", response_model=IngresoResponse)
def crear_ingreso(ingreso: IngresoCreate, db: Session = Depends(get_db)):
    return ingresos_crud.crear_ingreso(db=db, ingreso=ingreso)

@router.get("/", response_model=List[IngresoResponse])
def leer_ingresos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ingresos_crud.obtener_ingresos(db, skip, limit)