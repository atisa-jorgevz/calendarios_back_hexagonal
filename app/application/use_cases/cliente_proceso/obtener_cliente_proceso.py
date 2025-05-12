from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

def obtener_cliente_proceso(id: int, repo: ClienteProcesoRepository):
    return repo.obtener_por_id(id)
