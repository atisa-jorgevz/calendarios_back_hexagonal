from app.domain.repositories.proceso_repository import ProcesoRepository
from typing import Optional

def listar_procesos_cliente_por_empleado(
    email: str,
    repo: ProcesoRepository,
    mes: Optional[int] = None,
    anio: Optional[int] = None
):
    return repo.listar_procesos_cliente_por_empleado(
        email=email,
        mes=mes,
        anio=anio
    )
