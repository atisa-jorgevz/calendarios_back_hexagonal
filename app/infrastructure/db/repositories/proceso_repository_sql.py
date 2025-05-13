from app.domain.repositories.proceso_repository import ProcesoRepository
from app.domain.entities.proceso import Proceso
from sqlalchemy import text
from collections import OrderedDict
from app.infrastructure.db.models import ProcesoModel
from app.infrastructure.db.compartido.mis_clientes_cte import MIS_CLIENTES_CTE

SQL_TODO_EN_UNO = MIS_CLIENTES_CTE + """
SELECT
  mc.id_cliente             AS cliente_id,
  c.razsoc                  AS cliente_nombre,
  p.id                      AS proceso_id,
  p.nombre                  AS proceso_nombre,
  p.fecha_inicio            AS proceso_fecha_inicio,
  p.fecha_fin               AS proceso_fecha_fin
FROM mis_clientes mc
  JOIN [ATISA_Input].dbo.clientes c        ON c.idcliente   = mc.id_cliente
  JOIN [ATISA_Input].dbo.cliente_proceso cp ON cp.idcliente  = c.idcliente
  JOIN [ATISA_Input].dbo.proceso p         ON p.id          = cp.id_proceso
ORDER BY mc.id_cliente, p.id;
"""

class ProcesoRepositorySQL(ProcesoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, proceso: Proceso):
        modelo = ProcesoModel(**vars(proceso))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def actualizar(self, id: int, data: dict):
        proceso = self.session.query(ProcesoModel).filter_by(id=id).first()
        if not proceso:
            return None

        for key, value in data.items():
            setattr(proceso, key, value)

        self.session.commit()
        self.session.refresh(proceso)
        return proceso

    def listar(self):
        return self.session.query(ProcesoModel).all()
    
    def obtener_por_id(self, id: int):
        return self.session.query(ProcesoModel).filter_by(id=id).first()

    def eliminar(self, id: int):
        proceso = self.session.query(ProcesoModel).filter_by(id=id).first()
        if not proceso:
            return None
        self.session.delete(proceso)
        self.session.commit()
        return True

    def listar_procesos_cliente_por_empleado(self, email: str):
        
        result = self.session.execute(text(SQL_TODO_EN_UNO), {"email": email})        
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
            proc_map = clientes[cid]["procesos"]
            pid = r["proceso_id"]
            if pid not in proc_map:
                proc_map[pid] = {
                    "id": pid,
                    "nombre": r["proceso_nombre"],
                    "fecha_inicio": r["proceso_fecha_inicio"],
                    "fecha_fin": r["proceso_fecha_fin"]
                }

        resultado = []
        for entry in clientes.values():
            entry["procesos"] = list(entry["procesos"].values())
            resultado.append(entry)

        return resultado
        