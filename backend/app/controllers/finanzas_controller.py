from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import datetime
from typing import Dict, Any
from app.database.database import get_db
from app.models.gastos import Gasto
from app.models.ingresos import Ingreso
from app.models.viajes import Viaje

router = APIRouter(prefix="/finanzas", tags=["Finanzas"])

@router.get("/dashboard")
def obtener_metricas_dashboard(mes: int = datetime.now().month, anio: int = datetime.now().year, db: Session = Depends(get_db)):
    """Devuelve todos los datos calculados para los gráficos"""
    try:
        # Totales del mes
        total_ingresos = db.query(func.sum(Ingreso.monto)).filter(
            extract('month', Ingreso.fecha) == mes,
            extract('year', Ingreso.fecha) == anio
        ).scalar() or 0.0

        total_gastos = db.query(func.sum(Gasto.monto)).filter(
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).scalar() or 0.0

        # Para el grafico de barras
        ingresos_vs_gastos = [
            {"mes": f"{mes}/{anio}", "ingresos": total_ingresos, "gastos": total_gastos}
        ]

        # Para el grafico de toratas
        gastos_por_tipo_query = db.query(
            Gasto.tipo_gasto, 
            func.sum(Gasto.monto)
        ).filter(
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).group_by(Gasto.tipo_gasto).all()

        gastos_por_tipo = [
            {"nombre": tipo, "valor": monto} for tipo, monto in gastos_por_tipo_query
        ]

        # Para grafico de lineas
        combustible_query = db.query(
            extract('day', Gasto.fecha).label('dia'),
            func.sum(Gasto.monto).label('monto')
        ).filter(
            Gasto.tipo_gasto == 'COMBUSTIBLE',
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).group_by('dia').all()

        consumo_diario = [
            {"dia": str(int(dia)), "consumo": monto} for dia, monto in combustible_query
        ]

        # Los ultimos viajes
        ultimos_viajes = db.query(Viaje).order_by(Viaje.fecha_salida.desc()).limit(10).all()
        
        return {
            "metricas": {
                "ingresos_mes": total_ingresos,
                "gastos_mes": total_gastos,
                "balance": total_ingresos - total_gastos
            },
            "graficos": {
                "ingresos_gastos": ingresos_vs_gastos,
                "gastos_por_tipo": gastos_por_tipo,
                "consumo_combustible": consumo_diario
            },
            "viajes_tabla": ultimos_viajes
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))