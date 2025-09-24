from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.entities.proceso import Proceso
from app.application.services.generadores_temporalidad.factory import obtener_generador
from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from datetime import datetime

def generar_calendario_cliente_proceso(
    data,
    proceso_maestro: Proceso,
    repo: ClienteProcesoRepository,
    repo_hito_maestro: ProcesoHitoMaestroRepository,
    repo_hito_cliente: ClienteProcesoHitoRepository
):
    generador = obtener_generador(proceso_maestro.temporalidad)
    resultado = generador.generar(data, proceso_maestro, repo, repo_hito_maestro)

    # Crear hitos para cada ClienteProceso generado
    for cliente_proceso in resultado.get("procesos", []):
        hitos_maestros = repo_hito_maestro.listar_por_proceso(cliente_proceso.id_proceso)
        for proceso_hito_maestro, hito_data in hitos_maestros:
            nuevo_hito = ClienteProcesoHito(
                id=None,
                cliente_proceso_id=cliente_proceso.id,
                hito_id=hito_data.id,  # ID del hito (que coincide con proceso_hito_maestro.id_hito)
                estado="Nuevo",
                fecha_inicio=cliente_proceso.fecha_inicio,
                fecha_fin=None,
                hora_limite=hito_data.hora_limite,  # Del HitoModel
                fecha_estado=datetime.utcnow(),
                tipo=hito_data.tipo  # Del HitoModel
            )
            repo_hito_cliente.guardar(nuevo_hito)

    return {
        "mensaje": resultado.get("mensaje"),
        "cantidad": resultado.get("cantidad"),
        "anio": resultado.get("anio")
    }
