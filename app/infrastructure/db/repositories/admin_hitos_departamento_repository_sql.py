from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain.repositories.admin_hitos_departamento_repository import (
    AdminHitosDepartamentoRepository,
)


class AdminHitosDepartamentoRepositorySQL(AdminHitosDepartamentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def listar_hitos_departamentos(
        self,
        mes: Optional[int] = None,
        anio: Optional[int] = None,
        cod_subdepar: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        filtros = []
        params: Dict[str, Any] = {}

        if mes is not None:
            filtros.append("MONTH(cph.fecha_limite) = :mes")
            params["mes"] = mes
        if anio is not None:
            filtros.append("YEAR(cph.fecha_limite) = :anio")
            params["anio"] = anio
        if cod_subdepar:
            filtros.append("sd.codSubDePar = :cod_subdepar")
            params["cod_subdepar"] = cod_subdepar

        where_extra = (" AND " + " AND ".join(filtros)) if filtros else ""

        # Mantiene nombres físicos de tablas según el esquema existente
        sql = f"""
            SELECT 
                sd.codSubDePar      AS codigo_subdepar,
                sd.nombre           AS nombre_subdepar,
                p.id                AS proceso_id,
                p.nombre            AS proceso_nombre,
                h.id                AS hito_id,
                h.nombre            AS hito_nombre,
                cph.habilitado      AS habilitado,
                c.idcliente         AS cliente_id,
                c.razsoc            AS cliente_nombre,
                c.cif               AS cliente_cif,
                cph.id              AS cliente_proceso_hito_id,
                cph.cliente_proceso_id AS cliente_proceso_id,
                cph.estado          AS estado,
                COALESCE(cph.fecha_limite, h.fecha_limite) AS fecha_limite,
                COALESCE(cph.hora_limite, h.hora_limite)   AS hora_limite,
                cph.tipo            AS tipo
            FROM [ATISA_Input].dbo.cliente_proceso_hito cph
            JOIN [ATISA_Input].dbo.cliente_proceso cp ON cp.id = cph.cliente_proceso_id
            JOIN [ATISA_Input].dbo.proceso p ON p.id = cp.proceso_id
            JOIN [ATISA_Input].dbo.proceso_hito_maestro phm ON phm.hito_id = cph.hito_id AND phm.proceso_id = p.id
            JOIN [ATISA_Input].dbo.hito h ON h.id = phm.hito_id
            JOIN [ATISA_Input].dbo.clienteSubDepar csd ON csd.id = cp.cliente_id
            JOIN [ATISA_Input].dbo.clientes c ON c.idcliente = csd.id
            JOIN [ATISA_Input].dbo.SubDePar sd ON sd.codSubDePar = csd.codSubDePar
            WHERE 1=1 AND cph.habilitado = 1 {where_extra}
            ORDER BY sd.codSubDePar, p.id, h.id
        """

        result = self.session.execute(text(sql), params)
        rows = result.mappings().all()

        # Estructura agrupada por subdepartamento y proceso
        salida: List[Dict[str, Any]] = []
        agrupado: Dict[str, Dict[str, Any]] = {}

        for r in rows:
            clave_depar = r["codigo_subdepar"]
            if clave_depar not in agrupado:
                agrupado[clave_depar] = {
                    "departamento": {
                        "codigo": r["codigo_subdepar"],
                        "nombre": r["nombre_subdepar"],
                    },
                    "procesos": {},
                }

            dep = agrupado[clave_depar]
            pid = r["proceso_id"]
            if pid not in dep["procesos"]:
                dep["procesos"][pid] = {
                    "id": pid,
                    "nombre": r["proceso_nombre"],
                    "hitos": [],
                }

            dep["procesos"][pid]["hitos"].append(
                {
                    "id": r["hito_id"],
                    "cliente_proceso_id": r["cliente_proceso_id"],
                    "cliente_proceso_hito_id": r["cliente_proceso_hito_id"],
                    "nombre": r["hito_nombre"],
                    "habilitado": r["habilitado"],
                    "cliente": {
                        "id": r["cliente_id"],
                        "nombre": r["cliente_nombre"],
                        "cif": r["cliente_cif"],
                    },
                    "estado": r["estado"],
                    "fecha_limite": r["fecha_limite"],
                    "hora_limite": r["hora_limite"],
                    "tipo": r["tipo"],
                }
            )

        for dep in agrupado.values():
            dep["procesos"] = list(dep["procesos"].values())
            salida.append(dep)

        return salida

    def actualizar_hito_departamento(self, cliente_proceso_hito_id: int, data: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        Actualiza un registro de cliente_proceso_hito por ID.

        - Los campos estado, fecha_limite y hora_limite se actualizan en cliente_proceso_hito.
        - El campo tipo SIEMPRE se actualiza en la tabla hito (NUNCA en cliente_proceso_hito).

        Retorna el registro actualizado como dict o None si no existe.
        """
        # Validar claves permitidas para prevenir updates indeseados
        allowed_fields = {"estado", "fecha_limite", "hora_limite", "tipo"}
        update_fields = {k: v for k, v in data.items() if k in allowed_fields}
        if not update_fields:
            return None

        # Separar updates: CPH (estado/fechas) y HITO (tipo)
        cph_fields = {k: v for k, v in update_fields.items() if k in {"estado", "fecha_limite", "hora_limite"}}
        tipo_value = update_fields.get("tipo", None)

        # Ejecutar en una transacción
        try:
            # 1) Actualizar CPH si corresponde
            if cph_fields:
                set_clauses = []
                params_cph: Dict[str, Any] = {"id": cliente_proceso_hito_id}
                for k, v in cph_fields.items():
                    param_key = f"p_{k}"
                    set_clauses.append(f"{k} = :{param_key}")
                    params_cph[param_key] = v

                sql_update_cph = f"""
                    UPDATE [ATISA_Input].dbo.cliente_proceso_hito
                    SET {', '.join(set_clauses)}
                    WHERE id = :id
                """
                result_cph = self.session.execute(text(sql_update_cph), params_cph)
                if result_cph.rowcount == 0:
                    self.session.rollback()
                    return None

            # 2) Actualizar HITO.tipo si corresponde
            if tipo_value is not None:
                # Actualiza el HITO asociado al CPH recibido
                sql_update_hito = """
                    UPDATE h
                    SET h.tipo = :p_tipo
                    FROM [ATISA_Input].dbo.hito h
                    INNER JOIN [ATISA_Input].dbo.cliente_proceso_hito cph ON cph.hito_id = h.id
                    WHERE cph.id = :id
                """
                result_hito = self.session.execute(text(sql_update_hito), {"p_tipo": tipo_value, "id": cliente_proceso_hito_id})
                if result_hito.rowcount == 0:
                    # No existe CPH o HITO relacionado
                    self.session.rollback()
                    return None

            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        # Devolver el registro actualizado con un select detallado similar al listado
        sql_select = """
            SELECT 
                cph.id                AS cliente_proceso_hito_id,
                cph.cliente_proceso_id,
                cph.hito_id           AS hito_id,
                cph.estado,
                COALESCE(cph.fecha_limite, h.fecha_limite) AS fecha_limite,
                COALESCE(cph.hora_limite, h.hora_limite)   AS hora_limite,
                cph.habilitado        AS habilitado,
                cph.tipo              AS tipo
            FROM [ATISA_Input].dbo.cliente_proceso_hito cph
            JOIN [ATISA_Input].dbo.cliente_proceso cp ON cp.id = cph.cliente_proceso_id
            JOIN [ATISA_Input].dbo.hito h ON h.id = cph.hito_id
            WHERE cph.id = :id
        """
        row = self.session.execute(text(sql_select), {"id": cliente_proceso_hito_id}).mappings().first()
        return dict(row) if row else None
