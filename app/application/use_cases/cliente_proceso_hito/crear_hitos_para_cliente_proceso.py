from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

def crear_hitos_para_cliente_proceso(cliente_proceso, 
                                     repo_hito_maestro: ProcesoHitoMaestroRepository, 
                                     repo_hito_cliente: ClienteProcesoHitoRepository):
    """
    Genera hitos para un ClienteProceso usando las plantillas de ProcesoHitoMaestro.
    """
    hitos_maestros = repo_hito_maestro.listar_por_proceso(cliente_proceso.id_proceso)

    for hito in hitos_maestros:
        nuevo_hito = ClienteProcesoHito(
            id=None,
            id_cliente_proceso=cliente_proceso.id,
            id_hito=hito.id_hito,
            orden=hito.orden,
            dias_despues_inicio=hito.dias_despues_inicio,
            fecha=None  # Se calcula en otra lógica si se requiere
        )
        repo_hito_cliente.guardar(nuevo_hito)
