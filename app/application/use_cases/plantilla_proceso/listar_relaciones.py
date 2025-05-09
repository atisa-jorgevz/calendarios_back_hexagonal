from app.domain.repositories.plantilla_proceso_repository import PlantillaProcesoRepository

def listar_relaciones(repo: PlantillaProcesoRepository):
    return repo.listar()