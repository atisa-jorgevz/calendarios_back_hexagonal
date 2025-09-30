from datetime import timedelta, date
from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from .base_generador import GeneradorTemporalidad

class GeneradorQuincenal(GeneradorTemporalidad):
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository, repo_hito_maestro: ProcesoHitoMaestroRepository) -> dict:
        procesos_creados = []
        frecuencia = 15  # Días por quincena fija

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

        # Comenzar desde el primer día del año del primer hito
        # Si no hay fecha_inicio en el request, usar el día del primer hito
        if hasattr(data, 'fecha_inicio') and data.fecha_inicio:
            fecha_actual = data.fecha_inicio
        else:
            fecha_actual = date(anio, 1, primer_hito.fecha_inicio.day)

        while fecha_actual.year == anio:
            fecha_inicio = fecha_actual
            fecha_fin = fecha_actual + timedelta(days=frecuencia - 1)

            cliente_proceso = ClienteProceso(
                id=None,
                cliente_id=data.cliente_id,
                proceso_id=data.proceso_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                mes=fecha_inicio.month,
                anio=anio,
                anterior_id=None
            )
            procesos_creados.append(repo.guardar(cliente_proceso))
            fecha_actual = fecha_actual + timedelta(days=frecuencia)

        return {
            "mensaje": "Procesos cliente generados con éxito",
            "cantidad": len(procesos_creados),
            "anio": anio,
            "procesos": procesos_creados
        }
