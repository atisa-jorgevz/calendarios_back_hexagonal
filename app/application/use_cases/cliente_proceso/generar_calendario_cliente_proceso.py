from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.entities.proceso import Proceso
from app.application.services.generadores_temporalidad.factory import obtener_generador
from app.application.use_cases.cliente_proceso_hito.crear_hitos_para_cliente_proceso import crear_hitos_para_cliente_proceso

def generar_calendario_cliente_proceso(
    data,
    proceso_maestro: Proceso,
    repo: ClienteProcesoRepository,
    repo_hito_maestro: ProcesoHitoMaestroRepository,
    repo_hito_cliente: ClienteProcesoHitoRepository
):
    generador = obtener_generador(proceso_maestro.temporalidad)
    resultado = generador.generar(data, proceso_maestro, repo)

    # Crear hitos para cada ClienteProceso generado
    for cliente_proceso in resultado.get("procesos", []):
        crear_hitos_para_cliente_proceso(cliente_proceso, repo_hito_maestro, repo_hito_cliente)

    return {
        "mensaje": resultado.get("mensaje"),
        "cantidad": resultado.get("cantidad"),
        "anio": resultado.get("anio")
    }
