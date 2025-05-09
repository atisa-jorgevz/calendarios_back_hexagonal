import app.domain.entities.plantilla_proceso as PlantillaProceso
import app.domain.repositories.plantilla_proceso_repository as PlantillaProcesoRepository

def crear_relacion(data: dict, repo: PlantillaProcesoRepository):
    relacion = PlantillaProceso(
        id_proceso=data["id_proceso"],
        id_hito=data["id_hito"]
    )
    return repo.guardar(relacion)
