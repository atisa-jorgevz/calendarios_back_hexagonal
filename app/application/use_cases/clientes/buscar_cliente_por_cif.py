from app.domain.repositories.cliente_repository import ClienteRepository

def buscar_cliente_por_cif(cif: str, repo: ClienteRepository):
    return repo.buscar_por_cif(cif)
