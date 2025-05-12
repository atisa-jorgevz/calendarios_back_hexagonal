from app.domain.entities.plantilla_proceso import PlantillaProceso
from  app.domain.repositories.plantilla_proceso_repository import PlantillaProcesoRepository

def crear_relacion(data: dict, repo: PlantillaProcesoRepository):
    relacion = PlantillaProceso(
        proceso_id=data["proceso_id"],
        plantilla_id=data["plantilla_id"]
    )
    return repo.guardar(relacion)
