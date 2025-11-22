from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database.database import get_db
from app.schemas.gasto import GastoCreate, GastoResponse
from app.crud import gastos_crud

router = APIRouter(prefix="/gastos", tags=["Gastos"])

@router.post("/", response_model=GastoResponse)
def crear_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    return gastos_crud.crear_gasto(db=db, gasto=gasto)

@router.get("/", response_model=List[GastoResponse])
def leer_gastos(
    skip: int = 0, 
    limit: int = 100, 
    fecha_desde: Optional[date] = None,
    vehiculo_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return gastos_crud.obtener_gastos(db, skip, limit, fecha_desde, vehiculo_id=vehiculo_id)