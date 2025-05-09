from app.domain.repositories.proceso_repository import ProcesoRepository

def obtener_proceso(id: int, repo: ProcesoRepository):
    return repo.obtener_por_id(id)
