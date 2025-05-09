from app.domain.repositories.hito_repository import HitoRepository

def obtener_hito(id: int, repo: HitoRepository):
    return repo.obtener_por_id(id)
