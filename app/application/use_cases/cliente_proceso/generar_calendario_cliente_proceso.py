from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.entities.proceso import Proceso
from app.application.services.generadores_temporalidad.factory import obtener_generador

def generar_calendario_cliente_proceso(data, proceso_maestro: Proceso, repo: ClienteProcesoRepository):
    generador = obtener_generador(proceso_maestro.temporalidad)
    return generador.generar(data, proceso_maestro, repo)


