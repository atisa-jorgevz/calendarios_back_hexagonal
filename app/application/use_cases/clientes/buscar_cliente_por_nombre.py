from app.domain.repositories.cliente_repository import ClienteRepository

def buscar_cliente_por_nombre(nombre: str, repo: ClienteRepository):
    return repo.buscar_por_nombre(nombre)
