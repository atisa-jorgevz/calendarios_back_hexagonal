from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

def obtener_cliente_proceso_hitos_por_id(id: int, repo: ClienteProcesoHitoRepository):
    return repo.obtener_por_id(id)
