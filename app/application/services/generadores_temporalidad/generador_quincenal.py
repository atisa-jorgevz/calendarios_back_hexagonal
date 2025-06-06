from datetime import timedelta
from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from .base_generador import GeneradorTemporalidad
from app.infrastructure.mappers.cliente_proceso_mapper import mapear_modelo_a_entidad

class GeneradorQuincenal(GeneradorTemporalidad):
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository) -> dict:
        procesos_creados = []
        frecuencia = 15  # Días por quincena fija
        fecha_actual = data.fecha_inicio
        anio = fecha_actual.year

        while fecha_actual.year == anio:
            fecha_inicio = fecha_actual
            fecha_fin = fecha_actual + timedelta(days=frecuencia - 1)

            cliente_proceso = ClienteProceso(
                id=None,
                idcliente=data.idcliente,
                id_proceso=data.id_proceso,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                mes=fecha_inicio.month,
                anio=anio,
                id_anterior=None
            )
            procesos_creados.append(mapear_modelo_a_entidad(repo.guardar(cliente_proceso)))
            fecha_actual = fecha_actual + timedelta(days=frecuencia)

        return {
            "mensaje": "Procesos cliente generados con éxito",
            "cantidad": len(procesos_creados),
            "anio": anio,
            "procesos": procesos_creados
        }
