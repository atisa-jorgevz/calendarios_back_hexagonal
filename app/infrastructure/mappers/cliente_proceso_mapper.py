from app.domain.entities.cliente_proceso import ClienteProceso
from app.infrastructure.db.models.cliente_proceso_model import ClienteProcesoModel

def mapear_modelo_a_entidad(modelo: ClienteProcesoModel) -> ClienteProceso:
    return ClienteProceso(
        id=modelo.id,
        cliente_id=modelo.cliente_id,
        proceso_id=modelo.proceso_id,
        fecha_inicio=modelo.fecha_inicio,
        fecha_fin=modelo.fecha_fin,
        mes=modelo.mes,
        anio=modelo.anio,
        anterior_id=modelo.anterior_id
    )
def mapear_entidad_a_modelo(entidad: ClienteProceso) -> ClienteProcesoModel:
    return ClienteProcesoModel(
        id=entidad.id,
        cliente_id=entidad.cliente_id,
        proceso_id=entidad.proceso_id,
        fecha_inicio=entidad.fecha_inicio,
        fecha_fin=entidad.fecha_fin,
        mes=entidad.mes,
        anio=entidad.anio,
        anterior_id=entidad.anterior_id
    )
