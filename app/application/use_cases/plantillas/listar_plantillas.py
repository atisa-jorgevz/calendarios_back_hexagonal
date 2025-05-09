from app.domain.repositories.plantilla_repository import PlantillaRepository

def listar_plantillas(repo: PlantillaRepository):
    return repo.listar()
