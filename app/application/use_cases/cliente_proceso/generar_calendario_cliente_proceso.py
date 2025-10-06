from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.entities.proceso import Proceso
from app.application.services.generadores_temporalidad.factory import obtener_generador
from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from datetime import datetime, date, timedelta
from calendar import monthrange

def generar_calendario_cliente_proceso(
    data,
    proceso_maestro: Proceso,
    repo: ClienteProcesoRepository,
    repo_hito_maestro: ProcesoHitoMaestroRepository,
    repo_hito_cliente: ClienteProcesoHitoRepository
):
    generador = obtener_generador(proceso_maestro.temporalidad)
    resultado = generador.generar(data, proceso_maestro, repo, repo_hito_maestro)

    # Crear hitos para cada ClienteProceso generado
    for cliente_proceso in resultado.get("procesos", []):
        hitos_maestros = repo_hito_maestro.listar_por_proceso(cliente_proceso.proceso_id)
        for proceso_hito_maestro, hito_data in hitos_maestros:
            # Fecha límite del hito replicada en el mes/año del periodo
            base_year = cliente_proceso.fecha_fin.year if cliente_proceso.fecha_fin else cliente_proceso.fecha_inicio.year
            base_month = cliente_proceso.fecha_fin.month if cliente_proceso.fecha_fin else cliente_proceso.fecha_inicio.month
            dia_hito = hito_data.fecha_limite.day if hito_data.fecha_limite else 1
            _, last_day = monthrange(base_year, base_month)
            fecha_limite_instancia = date(base_year, base_month, min(dia_hito, last_day))
            # Ajustar fin de semana manteniendo SIEMPRE el mismo mes:
            # - Si es día 1 y cae en fin de semana: mover al lunes del mismo mes (1->2 si domingo; 1->3 si sábado)
            # - En otros casos: Sábado -> viernes (día - 1)
            #                   Domingo -> lunes (día + 1) si cabe en el mes; si no, viernes (día - 2)
            weekday = fecha_limite_instancia.weekday()  # 0=Lunes ... 5=Sábado, 6=Domingo
            if weekday == 5:  # Sábado
                if fecha_limite_instancia.day == 1:
                    # 1 sábado -> lunes 3
                    fecha_limite_instancia = fecha_limite_instancia + timedelta(days=2)
                else:
                    fecha_limite_instancia = fecha_limite_instancia - timedelta(days=1)
            elif weekday == 6:  # Domingo
                if fecha_limite_instancia.day == 1:
                    # 1 domingo -> lunes 2 (mismo mes)
                    fecha_limite_instancia = fecha_limite_instancia + timedelta(days=1)
                else:
                    # Resto de domingos -> viernes del mismo mes
                    fecha_limite_instancia = fecha_limite_instancia - timedelta(days=2)

            nuevo_hito = ClienteProcesoHito(
                id=None,
                cliente_proceso_id=cliente_proceso.id,
                hito_id=hito_data.id,
                estado="Nuevo",
                fecha_limite=fecha_limite_instancia,
                hora_limite=hito_data.hora_limite,
                fecha_estado=datetime.utcnow(),
                tipo=hito_data.tipo
            )
            repo_hito_cliente.guardar(nuevo_hito)

    return {
        "mensaje": resultado.get("mensaje"),
        "cantidad": resultado.get("cantidad"),
        "anio": resultado.get("anio")
    }
