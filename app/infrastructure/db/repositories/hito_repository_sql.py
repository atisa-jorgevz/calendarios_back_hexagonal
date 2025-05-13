from app.domain.repositories.hito_repository import HitoRepository
from app.domain.entities.hito import Hito
from app.infrastructure.db.models import HitoModel
from sqlalchemy import text
from collections import OrderedDict
from app.infrastructure.db.compartido.mis_clientes_cte import MIS_CLIENTES_CTE

SQL_HITOS_POR_EMPLEADO = MIS_CLIENTES_CTE + """
SELECT
  mc.id_cliente                     AS cliente_id,
  c.razsoc                          AS cliente_nombre,
  p.id                              AS proceso_id,
  p.nombre                          AS proceso_nombre,
  p.fecha_inicio                    AS proceso_fecha_inicio,
  p.fecha_fin                       AS proceso_fecha_fin,
  h.id                              AS hito_id,
  h.nombre                          AS hito_nombre,
  h.fecha_inicio                    AS hito_fecha_inicio,
  h.fecha_fin                       AS hito_fecha_fin
FROM mis_clientes mc
JOIN [ATISA_Input].dbo.clientes c                ON c.idcliente = mc.id_cliente
JOIN [ATISA_Input].dbo.cliente_proceso cp        ON cp.idcliente = c.idcliente
JOIN [ATISA_Input].dbo.proceso p                 ON p.id = cp.id_proceso
JOIN [ATISA_Input].dbo.cliente_proceso_hito cph  ON cph.cliente_proceso_id = cp.id
JOIN [ATISA_Input].dbo.hito h                    ON h.id = cph.hito_id
ORDER BY mc.id_cliente, p.id, h.id;
"""

class HitoRepositorySQL(HitoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, hito: Hito):
        modelo = HitoModel(**vars(hito))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def listar(self):
        return self.session.query(HitoModel).all()

    def obtener_por_id(self, id: int):
        return self.session.query(HitoModel).filter_by(id=id).first()

    def actualizar(self, id: int, data: dict):
        hito = self.obtener_por_id(id)
        if not hito:
            return None
        for key, value in data.items():
            setattr(hito, key, value)
        self.session.commit()
        self.session.refresh(hito)
        return hito

    def eliminar(self, id: int):
        hito = self.obtener_por_id(id)
        if not hito:
            return None
        self.session.delete(hito)
        self.session.commit()
        return True
    
    def listar_hitos_cliente_por_empleado(self, email: str):
        result = self.session.execute(text(SQL_HITOS_POR_EMPLEADO), {"email": email})
        rows = result.mappings().all()

        clientes = OrderedDict()
        for r in rows:
            cid = r["cliente_id"]
            if cid not in clientes:
                clientes[cid] = {
                    "cliente": {
                        "id": cid,
                        "nombre": r["cliente_nombre"]
                    },
                    "procesos": OrderedDict()
                }

            pid = r["proceso_id"]
            procesos = clientes[cid]["procesos"]
            if pid not in procesos:
                procesos[pid] = {
                    "id": pid,
                    "nombre": r["proceso_nombre"],
                    "fecha_inicio": r["proceso_fecha_inicio"],
                    "fecha_fin": r["proceso_fecha_fin"],
                    "hitos": []
                }

            procesos[pid]["hitos"].append({
                "id": r["hito_id"],
                "nombre": r["hito_nombre"],
                "fecha_inicio": r["hito_fecha_inicio"],
                "fecha_fin": r["hito_fecha_fin"]
            })

        resultado = []
        for entry in clientes.values():
            entry["procesos"] = list(entry["procesos"].values())
            resultado.append(entry)

        return resultado
