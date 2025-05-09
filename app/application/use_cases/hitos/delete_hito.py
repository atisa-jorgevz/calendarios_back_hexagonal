from app.domain.repositories.hito_repository import HitoRepository

def eliminar_hito(id: int, repo: HitoRepository):
    return repo.eliminar(id)
