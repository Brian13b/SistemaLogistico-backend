from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database.database import get_db
from app.schemas.ingresos_schemas import IngresoCreate, IngresoResponse
from app.crud import ingresos_crud

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])

@router.post("/", response_model=IngresoResponse)
async def crear_ingreso_endpoint(ingreso_data: str = Form(...), archivo: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        ingreso_dict = json.loads(ingreso_data)
        ingreso_schema = IngresoCreate(**ingreso_dict)
        return await ingresos_crud.crear_ingreso_con_archivo(db, ingreso_schema, archivo)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[IngresoResponse])
def leer_ingresos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ingresos_crud.obtener_ingresos(db, skip, limit)