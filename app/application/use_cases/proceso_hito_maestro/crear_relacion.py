from app.domain.entities.proceso_hito_maestro import ProcesoHitoMaestro
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository

def crear_relacion(data: dict, repo: ProcesoHitoMaestroRepository):
    relacion = ProcesoHitoMaestro(
        id_proceso=data["id_proceso"],
        id_hito=data["id_hito"]
    )
    return repo.guardar(relacion)
