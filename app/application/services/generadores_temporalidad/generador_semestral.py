from datetime import date
from calendar import monthrange
from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from .base_generador import GeneradorTemporalidad

class GeneradorSemestral(GeneradorTemporalidad):
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository, repo_hito_maestro: ProcesoHitoMaestroRepository) -> dict:
        procesos_creados = []

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
            dia_inicio = data.fecha_inicio.day
        else:
            dia_inicio = primer_hito.fecha_inicio.day

        fecha_actual = date(anio, 1, dia_inicio)

        while fecha_actual.year == anio and fecha_actual.month <= 12:
            mes_inicio = fecha_actual.month
            _, last_day_inicio = monthrange(anio, mes_inicio)
            fecha_inicio = date(anio, mes_inicio, min(fecha_actual.day, last_day_inicio))

            # Un semestre son 6 meses, así que el mes final será mes_inicio + 5
            mes_fin = min(mes_inicio + 5, 12)
            _, last_day_fin = monthrange(anio, mes_fin)
            fecha_fin = date(anio, mes_fin, last_day_fin)

            # Ajustar fechas basándose en los hitos del proceso
            # El primer hito define la fecha de inicio real del proceso
            if primer_hito.fecha_inicio:
                # Usar el día del primer hito pero del mes calculado
                fecha_inicio_real = date(anio, mes_inicio, min(primer_hito.fecha_inicio.day, last_day_inicio))
            else:
                fecha_inicio_real = fecha_inicio

            # El último hito define la fecha de fin real del proceso
            if ultimo_hito.fecha_fin:
                # Usar el día del último hito pero del mes calculado
                fecha_fin_real = date(anio, mes_fin, min(ultimo_hito.fecha_fin.day, last_day_fin))
            else:
                fecha_fin_real = fecha_fin

            cliente_proceso = ClienteProceso(
                id=None,
                cliente_id=data.cliente_id,
                proceso_id=data.proceso_id,
                fecha_inicio=fecha_inicio_real,
                fecha_fin=fecha_fin_real,
                mes=mes_inicio,
                anio=anio,
                anterior_id=None
            )
            procesos_creados.append(repo.guardar(cliente_proceso))

            # Avanzar 6 meses para el siguiente semestre
            if mes_inicio + 6 > 12:
                break
            fecha_actual = date(anio, mes_inicio + 6, 1)

        return {
            "mensaje": "Procesos cliente generados con éxito",
            "cantidad": len(procesos_creados),
            "anio": anio,
            "procesos": procesos_creados
        }
