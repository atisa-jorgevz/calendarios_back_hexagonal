from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository

def listar_relaciones(repo: ProcesoHitoMaestroRepository):
    return repo.listar()
