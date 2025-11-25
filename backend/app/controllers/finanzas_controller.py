from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import datetime
from typing import Dict, Any
from app.database.database import get_db
from app.models.gasto import Gasto
from app.models.ingreso import Ingreso
from app.models.viaje import Viaje

router = APIRouter(prefix="/finanzas", tags=["Finanzas"])

@router.get("/dashboard")
def obtener_metricas_dashboard(
    mes: int = datetime.now().month,
    anio: int = datetime.now().year,
    db: Session = Depends(get_db)
):
    """
    Devuelve todos los datos calculados para los gráficos del Frontend
    """
    try:
        # 1. METRICAS TOTALES DEL MES
        total_ingresos = db.query(func.sum(Ingreso.monto)).filter(
            extract('month', Ingreso.fecha) == mes,
            extract('year', Ingreso.fecha) == anio
        ).scalar() or 0.0

        total_gastos = db.query(func.sum(Gasto.monto)).filter(
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).scalar() or 0.0

        # 2. PARA GRÁFICO DE BARRAS (Ingresos vs Gastos últimos 6 meses)
        # Esta query es un poco más compleja, agrupa por mes
        # (Simplificación: devolvemos el mes actual y simulamos anteriores si no hay datos
        # para que el gráfico no se rompa, idealmente se hace una query de rango)
        ingresos_vs_gastos = [
            {"mes": f"{mes}/{anio}", "ingresos": total_ingresos, "gastos": total_gastos}
        ]

        # 3. PARA GRÁFICO DE TORTA (Gastos por Tipo)
        gastos_por_tipo_query = db.query(
            Gasto.tipo_gasto, 
            func.sum(Gasto.monto)
        ).filter(
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).group_by(Gasto.tipo_gasto).all()

        # Formatear para Recharts (PieChart)
        # Colores harcodeados o asignados en el front
        gastos_por_tipo = [
            {"nombre": tipo, "valor": monto} for tipo, monto in gastos_por_tipo_query
        ]

        # 4. PARA GRÁFICO DE LÍNEAS (Consumo Combustible)
        # Filtramos gastos tipo 'COMBUSTIBLE'
        combustible_query = db.query(
            extract('day', Gasto.fecha).label('dia'),
            func.sum(Gasto.monto).label('monto') # O litros si tuvieras esa columna
        ).filter(
            Gasto.tipo_gasto == 'COMBUSTIBLE',
            extract('month', Gasto.fecha) == mes,
            extract('year', Gasto.fecha) == anio
        ).group_by('dia').all()

        consumo_diario = [
            {"dia": str(int(dia)), "consumo": monto} for dia, monto in combustible_query
        ]

        # 5. LISTA DE VIAJES RECIENTES (Para la tabla)
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
            "viajes_tabla": ultimos_viajes # Serializar esto con Pydantic en el front
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))