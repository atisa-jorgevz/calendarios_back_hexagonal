from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

def listar_cliente_proceso_hitos(repo: ClienteProcesoHitoRepository):
    return repo.listar()
