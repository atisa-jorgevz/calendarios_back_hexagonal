from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_db
from app.application.services.metricas_service import MetricasService
from app.interfaces.schemas.metricas import (
    CumplimientoHitosSchema,
    HitosPorProcesoSchema,
    TiempoResolucionSchema,
    HitosVencidosSchema,
    ClientesInactivosSchema,
    VolumenMensualSchema,
    ResumenMetricasSchema
)

router = APIRouter()

@router.get("/cumplimiento-hitos", response_model=CumplimientoHitosSchema)
async def get_cumplimiento_hitos(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene el porcentaje de cumplimiento de hitos por cliente
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_cumplimiento_hitos(email)

@router.get("/hitos-por-proceso", response_model=HitosPorProcesoSchema)
async def get_hitos_por_proceso(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene el total de hitos abiertos/pendientes por tipo de proceso
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_hitos_por_proceso(email)

@router.get("/tiempo-resolucion", response_model=TiempoResolucionSchema)
async def get_tiempo_resolucion(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene el tiempo medio de resolución de hitos
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_tiempo_resolucion(email)

@router.get("/hitos-vencidos", response_model=HitosVencidosSchema)
async def get_hitos_vencidos(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene alertas de hitos vencidos sin cerrar
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_hitos_vencidos(email)

@router.get("/clientes-inactivos", response_model=ClientesInactivosSchema)
async def get_clientes_inactivos(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene clientes sin hitos activos
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_clientes_inactivos(email)

@router.get("/volumen-mensual", response_model=VolumenMensualSchema)
async def get_volumen_mensual(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene el volumen mensual de hitos
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_volumen_mensual(email)

@router.get("/resumen", response_model=ResumenMetricasSchema)
async def get_resumen_metricas(
    email: str = Query(..., description="Email del usuario para filtrar métricas"),
    db: Session = Depends(get_db)
):
    """
    Obtiene el resumen de todas las métricas para el dashboard general
    """
    metricas_service = MetricasService(db)
    return metricas_service.get_resumen_metricas(email)