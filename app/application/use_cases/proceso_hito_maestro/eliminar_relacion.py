from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository

def eliminar_relacion(id: int, repo: ProcesoHitoMaestroRepository):
    return repo.eliminar(id)