from datetime import date
from calendar import monthrange
from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from .base_generador import GeneradorTemporalidad

class GeneradorTrimestral(GeneradorTemporalidad):
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository) -> dict:
        procesos_creados = []
        fecha_actual = data.fecha_inicio
        anio = fecha_actual.year

        while fecha_actual.year == anio and fecha_actual.month <= 12:
            mes_inicio = fecha_actual.month
            _, last_day_inicio = monthrange(anio, mes_inicio)
            fecha_inicio = date(anio, mes_inicio, min(fecha_actual.day, last_day_inicio))

            mes_fin = min(mes_inicio + 2, 12)
            _, last_day_fin = monthrange(anio, mes_fin)
            fecha_fin = date(anio, mes_fin, last_day_fin)

            cliente_proceso = ClienteProceso(
                id=None,
                idcliente=data.idcliente,
                id_proceso=data.id_proceso,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                mes=mes_inicio,
                anio=anio,
                id_anterior=None
            )
            procesos_creados.append(repo.guardar(cliente_proceso))

            if mes_inicio + 3 > 12:
                break
            fecha_actual = date(anio, mes_inicio + 3, 1)

        return {
            "mensaje": "Procesos cliente generados con éxito",
            "cantidad": len(procesos_creados),
            "anio": anio,
            "procesos": procesos_creados
        }
