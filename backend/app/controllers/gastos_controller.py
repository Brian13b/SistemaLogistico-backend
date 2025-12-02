from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import date

from app.database.database import get_db
from app.schemas.gastos_schemas import GastoCreate, GastoResponse
from app.crud import gastos_crud

router = APIRouter(prefix="/gastos", tags=["Gastos"])

@router.post("/", response_model=GastoResponse)
async def crear_gasto_endpoint(gasto_data: str = Form(...), archivo: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        # Deserializar el JSON
        gasto_dict = json.loads(gasto_data)
        gasto_schema = GastoCreate(**gasto_dict)
        
        return await gastos_crud.crear_gasto_con_archivo(db, gasto_schema, archivo)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El campo gasto_data no es un JSON válido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/", response_model=List[GastoResponse])
def leer_gastos(skip: int = 0, limit: int = 100, fecha_desde: Optional[date] = None, vehiculo_id: Optional[int] = None, db: Session = Depends(get_db)):
    return gastos_crud.obtener_gastos(db, skip, limit, fecha_desde, None, vehiculo_id)