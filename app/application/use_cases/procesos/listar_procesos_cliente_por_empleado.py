from app.domain.repositories.proceso_repository import ProcesoRepository
from typing import Optional

def listar_procesos_cliente_por_empleado(
    email: str,
    repo: ProcesoRepository,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None
):
    return repo.listar_procesos_cliente_por_empleado(
        email=email,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        mes=mes,
        anio=anio
    )