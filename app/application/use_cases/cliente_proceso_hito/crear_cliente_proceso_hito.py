from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

def crear_cliente_proceso_hito(data: dict, repo: ClienteProcesoHitoRepository):
    hito = ClienteProcesoHito(
        cliente_proceso_id=data["cliente_proceso_id"],
        hito_id=data["hito_id"],
        estado=data["estado"],
        fecha_estado=data.get("fecha_estado")
    )
    return repo.guardar(hito)
