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
