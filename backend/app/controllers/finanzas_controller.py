from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.database import get_db
from app.crud import gastos_crud, ingresos_crud

router = APIRouter(prefix="/finanzas", tags=["Finanzas"])

@router.get("/dashboard")
def obtener_resumen_mensual(
    mes: int = datetime.now().month, 
    anio: int = datetime.now().year, 
    db: Session = Depends(get_db)
):
    """Devuelve el balance del mes para los gráficos"""
    
    # 1. Total Ingresos
    total_ingresos = ingresos_crud.obtener_resumen_ingresos(db, mes, anio)
    
    # 2. Gastos desglosados
    gastos_raw = gastos_crud.obtener_resumen_gastos(db, mes, anio)
    
    total_gastos = sum([g.total for g in gastos_raw])
    gastos_por_categoria = {g.tipo_gasto: g.total for g in gastos_raw}

    return {
        "periodo": f"{mes}/{anio}",
        "ingresos": total_ingresos,
        "gastos": total_gastos,
        "balance": total_ingresos - total_gastos,
        "detalle_gastos": gastos_por_categoria
    }