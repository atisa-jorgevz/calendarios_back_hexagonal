from app.domain.entities.plantilla import Plantilla
from app.domain.repositories.plantilla_repository import PlantillaRepository

def crear_plantilla(data: dict, repo: PlantillaRepository):
    plantilla = Plantilla(
        nombre=data.get("nombre"),
        descripcion=data.get("descripcion"),
    )
    return repo.guardar(plantilla)
