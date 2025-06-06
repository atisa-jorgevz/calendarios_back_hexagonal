from app.domain.entities.cliente_proceso import ClienteProceso
from app.infrastructure.db.models.cliente_proceso_model import ClienteProcesoModel

def mapear_modelo_a_entidad(modelo: ClienteProcesoModel) -> ClienteProceso:
    return ClienteProceso(
        id=modelo.id,
        idcliente=modelo.idcliente,
        id_proceso=modelo.id_proceso,
        fecha_inicio=modelo.fecha_inicio,
        fecha_fin=modelo.fecha_fin,
        mes=modelo.mes,
        anio=modelo.anio,
        id_anterior=modelo.id_anterior
    )
def mapear_entidad_a_modelo(entidad: ClienteProceso) -> ClienteProcesoModel:
    return ClienteProcesoModel(
        id=entidad.id,
        idcliente=entidad.idcliente,
        id_proceso=entidad.id_proceso,
        fecha_inicio=entidad.fecha_inicio,
        fecha_fin=entidad.fecha_fin,
        mes=entidad.mes,
        anio=entidad.anio,
        id_anterior=entidad.id_anterior
    )