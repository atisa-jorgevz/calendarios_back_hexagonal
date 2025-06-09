from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from datetime import datetime

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
            cliente_proceso_id=cliente_proceso.id,
            hito_id=hito.id_hito,
            estado="Nuevo",
            fecha_inicio=cliente_proceso.fecha_inicio,
            fecha_fin=None,
            fecha_estado=datetime.utcnow()
        )        
        repo_hito_cliente.guardar(nuevo_hito)
