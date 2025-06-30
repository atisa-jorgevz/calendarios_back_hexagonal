from pydantic import BaseModel
from typing import List

class CumplimientoHitosSchema(BaseModel):
    porcentajeGeneral: float
    tendencia: str

class ProcesoDataSchema(BaseModel):
    nombreProceso: str
    hitosPendientes: int
    hitosCompletados: int

class HitosPorProcesoSchema(BaseModel):
    totalPendientes: int
    tendencia: str
    procesoData: List[ProcesoDataSchema]

class ResolucionDataSchema(BaseModel):
    periodo: str
    tiempoMedio: float

class TiempoResolucionSchema(BaseModel):
    tiempoMedioDias: float
    tendencia: str
    resolucionData: List[ResolucionDataSchema]

class HitosVencidosSchema(BaseModel):
    totalVencidos: int
    tendencia: str

class ClientesInactivosSchema(BaseModel):
    totalInactivos: int
    tendencia: str

class VolumenDataSchema(BaseModel):
    mes: str
    hitosCreados: int
    hitosCompletados: int

class VolumenMensualSchema(BaseModel):
    totalMesActual: int
    tendencia: str
    volumenData: List[VolumenDataSchema]

class MetricaResumenNumericaSchema(BaseModel):
    valor: int
    tendencia: str

class ResumenMetricasSchema(BaseModel):
    hitosCompletados: MetricaResumenNumericaSchema
    hitosPendientes: MetricaResumenNumericaSchema
    hitosVencidos: MetricaResumenNumericaSchema
    clientesInactivos: MetricaResumenNumericaSchema