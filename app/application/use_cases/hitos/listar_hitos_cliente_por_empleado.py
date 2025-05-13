from app.domain.repositories.hito_repository import HitoRepository

def listar_hitos_cliente_por_empleado(email: str, repo: HitoRepository):
    return repo.listar_hitos_cliente_por_empleado(email)