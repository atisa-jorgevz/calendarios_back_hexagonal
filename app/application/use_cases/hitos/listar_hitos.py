from app.domain.repositories.hito_repository import HitoRepository

def listar_hitos(repo: HitoRepository):
    return repo.listar()
