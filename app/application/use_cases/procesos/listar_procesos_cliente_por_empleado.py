from app.domain.repositories.proceso_repository import ProcesoRepository

def listar_procesos_cliente_por_empleado(email: str, repo: ProcesoRepository):
    return repo.listar_procesos_cliente_por_empleado(email)