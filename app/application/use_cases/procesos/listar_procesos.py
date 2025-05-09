from app.domain.repositories.proceso_repository import ProcesoRepository

def listar_procesos(proceso_repository: ProcesoRepository):
    return proceso_repository.listar()

