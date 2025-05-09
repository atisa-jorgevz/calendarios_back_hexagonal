from app.domain.repositories.plantilla_proceso_repository import PlantillaProcesoRepository

def eliminar_relacion_por_plantilla(id_plantilla: int, repo: PlantillaProcesoRepository):
    return repo.eliminar_por_plantilla(id_plantilla)
