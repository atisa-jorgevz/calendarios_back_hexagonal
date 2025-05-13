MIS_CLIENTES_CTE = """
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
"""

def construir_sql_procesos_cliente_por_empleado(filtrar_fecha=False, filtrar_mes=False, filtrar_anio=False):
    filtros = []
    if filtrar_fecha:
        filtros.append("cp.fecha_inicio >= :fecha_inicio")
        filtros.append("cp.fecha_inicio <= :fecha_fin")        
    if filtrar_mes:
        filtros.append("MONTH(cp.fecha_inicio) = :mes")
    if filtrar_anio:
        filtros.append("YEAR(cp.fecha_inicio) = :anio")

    where_extra = " AND " + " AND ".join(filtros) if filtros else ""

    sql = MIS_CLIENTES_CTE + f"""
    SELECT
      mc.id_cliente AS cliente_id,
      c.razsoc AS cliente_nombre,
      p.id AS proceso_id,
      p.nombre AS proceso_nombre,
      cp.fecha_inicio AS proceso_fecha_inicio,
      cp.fecha_fin AS proceso_fecha_fin
    FROM mis_clientes mc
    JOIN [ATISA_Input].dbo.clientes c ON c.idcliente = mc.id_cliente
    JOIN [ATISA_Input].dbo.cliente_proceso cp ON cp.idcliente = c.idcliente
    JOIN [ATISA_Input].dbo.proceso p ON p.id = cp.id_proceso
    WHERE 1=1 {where_extra}
    ORDER BY mc.id_cliente, p.id;
    """
    return sql

def construir_sql_hitos_cliente_por_empleado(filtrar_fecha=False, filtrar_mes=False, filtrar_anio=False):
    filtros = []
    if filtrar_fecha:
        filtros.append("cph.fecha_inicio >= :fecha_inicio")
        filtros.append("cph.fecha_inicio <= :fecha_fin")
    if filtrar_mes:
        filtros.append("MONTH(cph.fecha_inicio) = :mes")
    if filtrar_anio:
        filtros.append("YEAR(cph.fecha_inicio) = :anio")

    where_extra = " AND " + " AND ".join(filtros) if filtros else ""

    sql = MIS_CLIENTES_CTE + f"""
    SELECT
      mc.id_cliente AS cliente_id,
      c.razsoc  AS cliente_nombre,
      p.id AS proceso_id,
      p.nombre AS proceso_nombre,
      cp.fecha_inicio,
      cp.fecha_fin,
      h.id AS hito_id,
      h.nombre AS hito_nombre,
      cph.fecha_inicio as fecha_inicio_hito, 
      cph.fecha_fin as fecha_fin_hito
    FROM mis_clientes mc
    JOIN [ATISA_Input].dbo.clientes c ON c.idcliente = mc.id_cliente
    JOIN [ATISA_Input].dbo.cliente_proceso cp ON cp.idcliente = c.idcliente
    JOIN [ATISA_Input].dbo.proceso p ON p.id = cp.id_proceso
    JOIN [ATISA_Input].dbo.cliente_proceso_hito cph ON cph.cliente_proceso_id = cp.id
    JOIN [ATISA_Input].dbo.hito h ON h.id = cph.hito_id
    WHERE 1=1 {where_extra}
    ORDER BY mc.id_cliente, p.id, h.id;
    """
    return sql
