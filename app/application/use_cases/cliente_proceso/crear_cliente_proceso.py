from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

def crear_cliente_proceso(data: dict, repo: ClienteProcesoRepository):
    cliente_proceso = ClienteProceso(
        id=None,  # se genera en BBDD
        idcliente=data["idcliente"],
        id_proceso=data["id_proceso"],
        fecha_inicio=data["fecha_inicio"],
        fecha_fin=data.get("fecha_fin"),
        mes=data.get("mes"),
        anio=data.get("anio"),
        id_anterior=data.get("id_anterior")
    )
    return repo.guardar(cliente_proceso)
