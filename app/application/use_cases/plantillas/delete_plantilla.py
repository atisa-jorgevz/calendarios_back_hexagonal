from app.domain.repositories.plantilla_repository import PlantillaRepository

def eliminar_plantilla(id: int, repo: PlantillaRepository):
    return repo.eliminar(id)