from app.domain.repositories.plantilla_proceso_repository import PlantillaProcesoRepository

def eliminar_relacion(id: int, repo: PlantillaProcesoRepository):
    return repo.eliminar(id)
