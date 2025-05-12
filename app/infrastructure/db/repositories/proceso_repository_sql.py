from app.domain.repositories.proceso_repository import ProcesoRepository
from app.domain.entities.proceso import Proceso
from sqlalchemy import text
from collections import OrderedDict
from app.infrastructure.db.models import ProcesoModel

SQL_TODO_EN_UNO = """ 
WITH mis_clientes AS (
  SELECT CS.id AS id_cliente
    FROM [BI DW RRHH DEV].dbo.Persona P
    JOIN [BI DW RRHH DEV].dbo.HDW_Cecos C ON P.Numeross = C.Numeross
    JOIN [ATISA_Input].dbo.SubDePar S ON LEFT(C.CODIDEPAR,29)=S.codidepar
    JOIN [ATISA_Input].dbo.clienteSubdepar CS ON S.codSubDePar=CS.codSubDePar
   WHERE P.email = :email AND C.FECHAFIN IS NULL

  UNION

  SELECT DISTINCT CACO.IDCLIENTE AS id_cliente
    FROM [BI DW RRHH DEV].dbo.Persona P
    JOIN [BI DW RRHH DEV].dbo.HDW_Cecos C ON P.Numeross=C.Numeross
    JOIN [ATISA_Input].dbo.SubDePar S ON LEFT(C.CODIDEPAR,29)=S.codidepar
    JOIN [ATISA_Input].dbo.ArtSubdepar ASU ON S.codSubDePar=ASU.codSubDePar
    JOIN [ATISA_Input].dbo.cuercontra CUCO ON ASU.codart=CUCO.idArticulo
    JOIN [ATISA_Input].dbo.cabecontra CACO ON CUCO.IDCONTRATO=CACO.IDCONTRATO
   WHERE P.email = :email AND C.FECHAFIN IS NULL

  UNION

  SELECT DISTINCT CACO.IDCLIENTE AS id_cliente
    FROM [BI DW RRHH DEV].dbo.Persona P
    JOIN [BI DW RRHH DEV].dbo.HDW_Cecos C ON P.Numeross=C.Numeross
    JOIN [ATISA_Input].dbo.SubDePar S ON LEFT(C.CODIDEPAR,29)=S.codidepar
    JOIN [ATISA_Input].dbo.artCeco ARTC ON S.ceco=ARTC.codCeco
    JOIN [ATISA_Input].dbo.cuercontra CUCO ON ARTC.codart=CUCO.idArticulo
    JOIN [ATISA_Input].dbo.cabecontra CACO ON CUCO.IDCONTRATO=CACO.IDCONTRATO
   WHERE P.email = :email AND C.FECHAFIN IS NULL
)
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

    def listar_procesos_y_hitos_por_empleado(self, email: str):
        # 1) Ejecuta la consulta
        result = self.session.execute(text(SQL_TODO_EN_UNO), {"email": email})
        # 2) Convierte a diccionarios
        rows = result.mappings().all()

        # 3) Mapea a Cliente → [Procesos]
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

        # 4) Convierte los OrderedDict a listas
        resultado = []
        for entry in clientes.values():
            entry["procesos"] = list(entry["procesos"].values())
            resultado.append(entry)

        return resultado
        