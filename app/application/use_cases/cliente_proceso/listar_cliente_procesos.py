from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

def listar_cliente_procesos(repo: ClienteProcesoRepository):
    return repo.listar()
