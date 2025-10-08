from typing import List, Dict, Any, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.db.compartido.mis_clientes_cte import MIS_CLIENTES_CTE

class MetricasService:
    def __init__(self, db: Session):
        self.db = db

    def _calcular_tendencia(self, valor_actual: float, valor_anterior: float) -> str:
        """Calcula la tendencia porcentual entre dos valores"""
        if valor_anterior == 0:
            if valor_actual > 0:
                return "+100.0%"
            else:
                return "0.0%"

        cambio = ((valor_actual - valor_anterior) / valor_anterior) * 100
        signo = "+" if cambio >= 0 else ""
        return f"{signo}{cambio:.1f}%"

    def get_cumplimiento_hitos(self, email: str) -> Dict[str, Any]:
        """Obtiene porcentaje de cumplimiento de hitos por cliente"""
        # Consulta para últimos 30 días
        sql_actual = MIS_CLIENTES_CTE + """
        SELECT
            COUNT(cph.id) AS hitos_totales,
            COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -30, GETDATE())
        """

        # Consulta para 30 días anteriores (días 31-60)
        sql_anterior = MIS_CLIENTES_CTE + """
        SELECT
            COUNT(cph.id) AS hitos_totales,
            COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -60, GETDATE())
          AND cph.fecha_inicio < DATEADD(day, -30, GETDATE())
        """

        # Consulta general para todos los hitos
        sql_general = MIS_CLIENTES_CTE + """
        SELECT
            COUNT(cph.id) AS hitos_totales,
            COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        """

        result_actual = self.db.execute(text(sql_actual), {"email": email}).fetchone()
        result_anterior = self.db.execute(text(sql_anterior), {"email": email}).fetchone()
        result_general = self.db.execute(text(sql_general), {"email": email}).fetchone()

        # Calcular porcentaje general
        porcentaje_general = 0.0
        if result_general and result_general.hitos_totales > 0:
            porcentaje_general = round((result_general.hitos_completados * 100.0) / result_general.hitos_totales, 2)

        # Calcular tendencia
        porcentaje_actual = 0.0
        porcentaje_anterior = 0.0

        if result_actual and result_actual.hitos_totales > 0:
            porcentaje_actual = (result_actual.hitos_completados * 100.0) / result_actual.hitos_totales

        if result_anterior and result_anterior.hitos_totales > 0:
            porcentaje_anterior = (result_anterior.hitos_completados * 100.0) / result_anterior.hitos_totales

        tendencia = self._calcular_tendencia(porcentaje_actual, porcentaje_anterior)

        return {
            "porcentajeGeneral": porcentaje_general,
            "tendencia": tendencia
        }

    def get_hitos_por_proceso(self, email: str) -> Dict[str, Any]:
        """Obtiene total de hitos abiertos/pendientes por tipo de proceso"""
        sql = MIS_CLIENTES_CTE + """
        SELECT
            p.id AS proceso_id,
            LTRIM(RTRIM(p.nombre)) AS proceso_nombre,
            COUNT(CASE WHEN cph.estado != 'Finalizado' THEN 1 END) AS hitos_pendientes,
            COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN proceso p ON p.id = cp.id_proceso
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        GROUP BY p.id, p.nombre
        ORDER BY p.nombre
        """

        result = self.db.execute(text(sql), {"email": email}).fetchall()

        total_pendientes = sum(row.hitos_pendientes for row in result)

        proceso_data = []
        for row in result:
            proceso_data.append({
                "nombreProceso": str(row.proceso_nombre or "").strip(),
                "hitosPendientes": int(row.hitos_pendientes) if row.hitos_pendientes else 0,
                "hitosCompletados": int(row.hitos_completados) if row.hitos_completados else 0
            })

        # Calcular tendencia para hitos pendientes
        sql_actual_pendientes = MIS_CLIENTES_CTE + """
        SELECT COUNT(CASE WHEN cph.estado != 'Finalizado' THEN 1 END) AS pendientes_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -30, GETDATE())
        """

        sql_anterior_pendientes = MIS_CLIENTES_CTE + """
        SELECT COUNT(CASE WHEN cph.estado != 'Finalizado' THEN 1 END) AS pendientes_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -60, GETDATE())
          AND cph.fecha_inicio < DATEADD(day, -30, GETDATE())
        """

        result_actual_pend = self.db.execute(text(sql_actual_pendientes), {"email": email}).fetchone()
        result_anterior_pend = self.db.execute(text(sql_anterior_pendientes), {"email": email}).fetchone()

        pendientes_actual = result_actual_pend.pendientes_actual if result_actual_pend else 0
        pendientes_anterior = result_anterior_pend.pendientes_anterior if result_anterior_pend else 0

        tendencia = self._calcular_tendencia(float(pendientes_actual), float(pendientes_anterior))

        return {
            "totalPendientes": total_pendientes,
            "tendencia": tendencia,
            "procesoData": proceso_data
        }

    def get_tiempo_resolucion(self, email: str) -> Dict[str, Any]:
        """Obtiene tiempo medio de resolución de hitos"""
        sql = MIS_CLIENTES_CTE + """
        SELECT
            FORMAT(cph.fecha_limite, 'yyyy-MM') AS periodo,
            AVG(CASE
                WHEN cph.estado = 'Finalizado' THEN
                    DATEDIFF(day, cph.fecha_limite, CAST(cph.fecha_estado AS DATE))
                ELSE NULL
            END) AS tiempo_medio
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado = 'Finalizado'
          AND cph.fecha_limite >= DATEADD(month, -6, GETDATE())
        GROUP BY FORMAT(cph.fecha_limite, 'yyyy-MM')
        ORDER BY FORMAT(cph.fecha_limite, 'yyyy-MM')
        """

        result = self.db.execute(text(sql), {"email": email}).fetchall()

        tiempo_medio_general = 0.0
        resolucion_data = []

        if result:
            # Calcular promedio general
            total_tiempo = sum(float(row.tiempo_medio or 0) for row in result)
            tiempo_medio_general = round(total_tiempo / len(result), 2) if len(result) > 0 else 0.0

            # Convertir período a nombre de mes
            meses = {
                "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr",
                "05": "May", "06": "Jun", "07": "Jul", "08": "Ago",
                "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
            }

            for row in result:
                if row.tiempo_medio and row.periodo:
                    # Extraer mes del formato yyyy-MM
                    mes_num = row.periodo.split('-')[1] if '-' in row.periodo else "01"
                    mes_nombre = meses.get(mes_num, row.periodo)

                    resolucion_data.append({
                        "periodo": mes_nombre,
                        "tiempoMedio": round(float(row.tiempo_medio), 2)
                    })

        # Calcular tendencia para tiempo de resolución
        sql_actual_tiempo = MIS_CLIENTES_CTE + """
        SELECT AVG(CASE
            WHEN cph.estado = 'Finalizado' THEN
                DATEDIFF(day, cph.fecha_inicio, CAST(cph.fecha_estado AS DATE))
            ELSE NULL
        END) AS tiempo_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado = 'Finalizado'
          AND CAST(cph.fecha_estado AS DATE) >= DATEADD(day, -30, GETDATE())
        """

        sql_anterior_tiempo = MIS_CLIENTES_CTE + """
        SELECT AVG(CASE
            WHEN cph.estado = 'Finalizado' THEN
                DATEDIFF(day, cph.fecha_inicio, CAST(cph.fecha_estado AS DATE))
            ELSE NULL
        END) AS tiempo_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado = 'Finalizado'
          AND CAST(cph.fecha_estado AS DATE) >= DATEADD(day, -60, GETDATE())
          AND CAST(cph.fecha_estado AS DATE) < DATEADD(day, -30, GETDATE())
        """

        result_actual_tiempo = self.db.execute(text(sql_actual_tiempo), {"email": email}).fetchone()
        result_anterior_tiempo = self.db.execute(text(sql_anterior_tiempo), {"email": email}).fetchone()

        tiempo_actual = float(result_actual_tiempo.tiempo_actual or 0) if result_actual_tiempo else 0.0
        tiempo_anterior = float(result_anterior_tiempo.tiempo_anterior or 0) if result_anterior_tiempo else 0.0

        tendencia_tiempo = self._calcular_tendencia(tiempo_actual, tiempo_anterior)

        return {
            "tiempoMedioDias": tiempo_medio_general,
            "tendencia": tendencia_tiempo,
            "resolucionData": resolucion_data
        }

    def get_hitos_vencidos(self, email: str) -> Dict[str, Any]:
        """Obtiene alertas de hitos vencidos sin cerrar"""
        sql = MIS_CLIENTES_CTE + """
        SELECT
            cph.id AS hito_id,
            LTRIM(RTRIM(c.razsoc)) AS cliente_nombre,
            LTRIM(RTRIM(p.nombre)) AS proceso_nombre,
            FORMAT(cph.fecha_inicio, 'yyyy-MM-dd') AS fecha_vencimiento,
            DATEDIFF(day, cph.fecha_inicio, GETDATE()) AS dias_vencido
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN proceso p ON p.id = cp.id_proceso
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado != 'Finalizado'
          AND cph.fecha_inicio < GETDATE()
        ORDER BY dias_vencido DESC
        """

        result = self.db.execute(text(sql), {"email": email}).fetchall()

        # Calcular tendencia para hitos vencidos
        sql_actual_vencidos = MIS_CLIENTES_CTE + """
        SELECT COUNT(*) AS vencidos_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado != 'Finalizado'
          AND cph.fecha_inicio < GETDATE()
          AND cph.fecha_inicio >= DATEADD(day, -30, GETDATE())
        """

        sql_anterior_vencidos = MIS_CLIENTES_CTE + """
        SELECT COUNT(*) AS vencidos_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado != 'Finalizado'
          AND cph.fecha_inicio < DATEADD(day, -30, GETDATE())
          AND cph.fecha_inicio >= DATEADD(day, -60, GETDATE())
        """

        result_actual_venc = self.db.execute(text(sql_actual_vencidos), {"email": email}).fetchone()
        result_anterior_venc = self.db.execute(text(sql_anterior_vencidos), {"email": email}).fetchone()

        vencidos_actual = result_actual_venc.vencidos_actual if result_actual_venc else 0
        vencidos_anterior = result_anterior_venc.vencidos_anterior if result_anterior_venc else 0

        tendencia_vencidos = self._calcular_tendencia(float(vencidos_actual), float(vencidos_anterior))

        return {
            "totalVencidos": len(result),
            "tendencia": tendencia_vencidos
        }

    def get_clientes_inactivos(self, email: str) -> Dict[str, Any]:
        """Obtiene clientes sin hitos activos"""
        sql = MIS_CLIENTES_CTE + """
        SELECT
            mc.id_cliente AS cliente_id,
            LTRIM(RTRIM(c.razsoc)) AS cliente_nombre,
            FORMAT(MAX(cph.fecha_inicio), 'yyyy-MM-dd') AS ultima_actividad,
            DATEDIFF(day, MAX(cph.fecha_inicio), GETDATE()) AS dias_inactivo
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        LEFT JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        LEFT JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        GROUP BY mc.id_cliente, c.razsoc
        HAVING MAX(cph.fecha_inicio) IS NULL
           OR MAX(cph.fecha_inicio) < DATEADD(day, -30, GETDATE())
        ORDER BY dias_inactivo DESC
        """

        result = self.db.execute(text(sql), {"email": email}).fetchall()

        # Calcular tendencia para clientes inactivos
        sql_actual_inactivos = MIS_CLIENTES_CTE + """
        SELECT COUNT(DISTINCT mc.id_cliente) AS inactivos_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        LEFT JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        LEFT JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE (SELECT MAX(cph2.fecha_inicio)
               FROM cliente_proceso cp2
               JOIN cliente_proceso_hito cph2 ON cph2.cliente_proceso_id = cp2.id
               WHERE cp2.idcliente = mc.id_cliente) < DATEADD(day, -30, GETDATE())
           OR NOT EXISTS (SELECT 1 FROM cliente_proceso cp3 WHERE cp3.idcliente = mc.id_cliente)
        """

        sql_anterior_inactivos = MIS_CLIENTES_CTE + """
        SELECT COUNT(DISTINCT mc.id_cliente) AS inactivos_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        LEFT JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        LEFT JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE (SELECT MAX(cph2.fecha_inicio)
               FROM cliente_proceso cp2
               JOIN cliente_proceso_hito cph2 ON cph2.cliente_proceso_id = cp2.id
               WHERE cp2.idcliente = mc.id_cliente) < DATEADD(day, -60, GETDATE())
           OR NOT EXISTS (SELECT 1 FROM cliente_proceso cp3 WHERE cp3.idcliente = mc.id_cliente)
        """

        result_actual_inact = self.db.execute(text(sql_actual_inactivos), {"email": email}).fetchone()
        result_anterior_inact = self.db.execute(text(sql_anterior_inactivos), {"email": email}).fetchone()

        inactivos_actual = result_actual_inact.inactivos_actual if result_actual_inact else 0
        inactivos_anterior = result_anterior_inact.inactivos_anterior if result_anterior_inact else 0

        tendencia_inactivos = self._calcular_tendencia(float(inactivos_actual), float(inactivos_anterior))

        return {
            "totalInactivos": len(result),
            "tendencia": tendencia_inactivos
        }

    def get_volumen_mensual(self, email: str) -> Dict[str, Any]:
        """Obtiene volumen mensual de hitos"""
        sql = MIS_CLIENTES_CTE + """
        SELECT
            FORMAT(cph.fecha_inicio, 'yyyy-MM') AS mes,
            COUNT(cph.id) AS hitos_creados,
            COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(month, -6, GETDATE())
        GROUP BY FORMAT(cph.fecha_inicio, 'yyyy-MM')
        ORDER BY FORMAT(cph.fecha_inicio, 'yyyy-MM')
        """

        result = self.db.execute(text(sql), {"email": email}).fetchall()

        total_mes_actual = 0
        volumen_data = []

        if result:
            # El mes actual es el último en orden cronológico
            total_mes_actual = result[-1].hitos_creados if result else 0

            # Convertir período a nombre de mes
            meses = {
                "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr",
                "05": "May", "06": "Jun", "07": "Jul", "08": "Ago",
                "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
            }

            for row in result:
                if row.mes:
                    # Extraer mes del formato yyyy-MM
                    mes_num = row.mes.split('-')[1] if '-' in row.mes else "01"
                    mes_nombre = meses.get(mes_num, row.mes)

                    volumen_data.append({
                        "mes": mes_nombre,
                        "hitosCreados": int(row.hitos_creados) if row.hitos_creados else 0,
                        "hitosCompletados": int(row.hitos_completados) if row.hitos_completados else 0
                    })

        # Calcular tendencia para volumen mensual
        sql_actual_volumen = MIS_CLIENTES_CTE + """
        SELECT COUNT(cph.id) AS volumen_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -30, GETDATE())
        """

        sql_anterior_volumen = MIS_CLIENTES_CTE + """
        SELECT COUNT(cph.id) AS volumen_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.fecha_inicio >= DATEADD(day, -60, GETDATE())
          AND cph.fecha_inicio < DATEADD(day, -30, GETDATE())
        """

        result_actual_vol = self.db.execute(text(sql_actual_volumen), {"email": email}).fetchone()
        result_anterior_vol = self.db.execute(text(sql_anterior_volumen), {"email": email}).fetchone()

        volumen_actual = result_actual_vol.volumen_actual if result_actual_vol else 0
        volumen_anterior = result_anterior_vol.volumen_anterior if result_anterior_vol else 0

        tendencia_volumen = self._calcular_tendencia(float(volumen_actual), float(volumen_anterior))

        return {
            "totalMesActual": total_mes_actual,
            "tendencia": tendencia_volumen,
            "volumenData": volumen_data
        }

    def get_resumen_metricas(self, email: str) -> Dict[str, Any]:
        """Obtiene resumen de todas las métricas"""
        # Obtener cantidad total de hitos completados
        sql_hitos_completados = MIS_CLIENTES_CTE + """
        SELECT COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS hitos_completados
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        """

        result_completados = self.db.execute(text(sql_hitos_completados), {"email": email}).fetchone()
        total_completados = result_completados.hitos_completados if result_completados else 0

        # Calcular tendencia para hitos completados (cantidad, no porcentaje)
        sql_actual_completados = MIS_CLIENTES_CTE + """
        SELECT COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS completados_actual
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado = 'Finalizado'
          AND CAST(cph.fecha_estado AS DATE) >= DATEADD(day, -30, GETDATE())
        """

        sql_anterior_completados = MIS_CLIENTES_CTE + """
        SELECT COUNT(CASE WHEN cph.estado = 'Finalizado' THEN 1 END) AS completados_anterior
        FROM mis_clientes mc
        JOIN clientes c ON c.idcliente = mc.id_cliente
        JOIN cliente_proceso cp ON cp.idcliente = c.idcliente
        JOIN cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
        WHERE cph.estado = 'Finalizado'
          AND CAST(cph.fecha_estado AS DATE) >= DATEADD(day, -60, GETDATE())
          AND CAST(cph.fecha_estado AS DATE) < DATEADD(day, -30, GETDATE())
        """

        result_actual_comp = self.db.execute(text(sql_actual_completados), {"email": email}).fetchone()
        result_anterior_comp = self.db.execute(text(sql_anterior_completados), {"email": email}).fetchone()

        completados_actual = result_actual_comp.completados_actual if result_actual_comp else 0
        completados_anterior = result_anterior_comp.completados_anterior if result_anterior_comp else 0

        tendencia_completados = self._calcular_tendencia(float(completados_actual), float(completados_anterior))

        # Obtener otras métricas
        hitos_proceso = self.get_hitos_por_proceso(email)
        vencidos = self.get_hitos_vencidos(email)
        inactivos = self.get_clientes_inactivos(email)

        return {
            "hitosCompletados": {
                "valor": total_completados,  # Número de hitos completados, no porcentaje
                "tendencia": tendencia_completados
            },
            "hitosPendientes": {
                "valor": hitos_proceso['totalPendientes'],
                "tendencia": hitos_proceso['tendencia']
            },
            "hitosVencidos": {
                "valor": vencidos['totalVencidos'],
                "tendencia": vencidos['tendencia']
            },
            "clientesInactivos": {
                "valor": inactivos['totalInactivos'],
                "tendencia": inactivos['tendencia']
            }
        }
