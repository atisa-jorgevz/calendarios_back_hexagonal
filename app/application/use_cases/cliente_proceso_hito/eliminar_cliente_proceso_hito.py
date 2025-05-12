from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

def eliminar_cliente_proceso_hito(id: int, repo: ClienteProcesoHitoRepository):
    return repo.eliminar(id)
