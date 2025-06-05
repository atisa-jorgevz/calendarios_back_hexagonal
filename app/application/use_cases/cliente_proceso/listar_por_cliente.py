from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

def listar_por_cliente(id_cliente: int, repo: ClienteProcesoRepository):
    return repo.listar_por_cliente(id_cliente)