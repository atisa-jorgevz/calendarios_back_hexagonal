from datetime import date
from calendar import monthrange
from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from .base_generador import GeneradorTemporalidad

class GeneradorMensual(GeneradorTemporalidad):
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository, repo_hito_maestro: ProcesoHitoMaestroRepository) -> dict:
        procesos_creados = []
        frecuencia = 1

        # Obtener hitos del proceso maestro
        hitos_maestros = repo_hito_maestro.listar_por_proceso(proceso_maestro.id)

        if not hitos_maestros:
            raise ValueError(f"No se encontraron hitos para el proceso {proceso_maestro.id}")

        # Ordenar hitos por fecha de inicio para obtener el primero y último
        hitos_ordenados = sorted(hitos_maestros, key=lambda x: x[1].fecha_inicio)
        primer_hito = hitos_ordenados[0][1]  # HitoModel
        ultimo_hito = hitos_ordenados[-1][1]  # HitoModel

        # Usar el año de la fecha de inicio del primer hito como base
        anio = primer_hito.fecha_inicio.year

        # Comenzar desde enero del año del primer hito
        # Si no hay fecha_inicio en el request, usar el día del primer hito
        if hasattr(data, 'fecha_inicio') and data.fecha_inicio:
            fecha_actual = data.fecha_inicio
        else:
            fecha_actual = date(anio, 1, primer_hito.fecha_inicio.day)

        while fecha_actual.year == anio and fecha_actual.month <= 12:
            mes_inicio = fecha_actual.month
            _, last_day = monthrange(anio, mes_inicio)
            dia_inicio = fecha_actual.day if mes_inicio == fecha_actual.month else primer_hito.fecha_inicio.day
            fecha_inicio = date(anio, mes_inicio, min(dia_inicio, last_day))

            mes_fin = min(mes_inicio + frecuencia - 1, 12)
            _, last_day_fin = monthrange(anio, mes_fin)
            fecha_fin = date(anio, mes_fin, last_day_fin)

            cliente_proceso = ClienteProceso(
                id=None,
                cliente_id=data.cliente_id,
                proceso_id=data.proceso_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                mes=mes_inicio,
                anio=anio,
                anterior_id=None
            )

            procesos_creados.append(repo.guardar(cliente_proceso))
            if mes_inicio + frecuencia > 12:
                break
            fecha_actual = date(anio, mes_inicio + frecuencia, 1)

        return {
            "mensaje": "Procesos cliente generados con éxito",
            "cantidad": len(procesos_creados),
            "anio": anio,
            "procesos": procesos_creados
        }
