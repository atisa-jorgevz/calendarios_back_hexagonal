from app.domain.repositories.plantilla_repository import PlantillaRepository

def obtener_plantilla(id: int, repo: PlantillaRepository):
    return repo.obtener_por_id(id)
