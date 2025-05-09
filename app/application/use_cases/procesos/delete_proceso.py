from app.domain.repositories.proceso_repository import ProcesoRepository

def eliminar_proceso(id: int, repo: ProcesoRepository):
    return repo.eliminar(id)

