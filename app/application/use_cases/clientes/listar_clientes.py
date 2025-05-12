from app.domain.repositories.cliente_repository import ClienteRepository

def listar_clientes(repo: ClienteRepository):
    return repo.listar()
