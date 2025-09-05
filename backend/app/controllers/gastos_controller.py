from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.schemas.gastos_schemas import Gasto, GastoCreate
from app.crud.gastos_crud import crear_gasto, exportar_gastos, obtener_gastos, obtener_gasto, eliminar_gasto, obtener_gastos_por_viaje
from app.database.database import get_db
from app.services.gastos_pdf import generar_pdf_gastos

router = APIRouter()

@router.post("/gastos/", response_model=Gasto)
def crear_gasto_endpoint(gasto: GastoCreate, db: Session = Depends(get_db)):
    return crear_gasto(db, gasto)

@router.get("/gastos/", response_model=list[Gasto])
def obtener_gastos_endpoint(db: Session = Depends(get_db)):
    return obtener_gastos(db)

@router.get("/gastos/{gasto_id}", response_model=Gasto)
def obtener_gasto_endpoint(gasto_id: int, db: Session = Depends(get_db)):
    gasto = obtener_gasto(db, gasto_id)
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto

@router.get("/gastos/viaje/{viaje_id}", response_model=list[Gasto])
def obtener_gastos_por_viaje_endpoint(viaje_id: int, db: Session = Depends(get_db)):
    return obtener_gastos_por_viaje(db, viaje_id=viaje_id)

@router.delete("/gastos/{gasto_id}", response_model=Gasto)
def eliminar_gasto_endpoint(gasto_id: int, db: Session = Depends(get_db)):
    gasto = eliminar_gasto(db, gasto_id)
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto

@router.get("/gastos/exportar_pdf")
def exportar_gastos_pdf_endpoint(db: Session = Depends(get_db), viaje_id: int = None, cantidad: int = None, rango: str = None):
    gastos = exportar_gastos(db, viaje_id=viaje_id, cantidad=cantidad, rango=rango)
    buffer = generar_pdf_gastos(gastos)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=gastos.pdf"})