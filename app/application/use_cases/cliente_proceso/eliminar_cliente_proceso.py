from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

def eliminar_cliente_proceso(id: int, repo: ClienteProcesoRepository):
    return repo.eliminar(id)
