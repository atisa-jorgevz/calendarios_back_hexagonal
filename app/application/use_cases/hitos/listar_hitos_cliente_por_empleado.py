from app.domain.repositories.hito_repository import HitoRepository
from typing import Optional

def listar_hitos_cliente_por_empleado(
    email: str,     
    repo: HitoRepository,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None    
):
    return repo.listar_hitos_cliente_por_empleado( 
        email= email,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        mes=mes,
        anio=anio
    )

