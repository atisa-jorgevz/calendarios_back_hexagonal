from sqlalchemy import text
from sqlalchemy.orm import Session

class EmpleadoCecoProvider:

    def __init__(self, db: Session):
        self.db = db

    def obtener_cecos_por_email(self, email: str) -> list[str]:
        sql = text("""
        SELECT s.ceco
        FROM [ATISA_Input].[dbo].[subDepar] s
        JOIN [BI DW RRHH DEV].[dbo].[HDW_Cecos] c
            ON s.codidepar = c.CODIDEPAR
        JOIN [BI DW RRHH DEV].[dbo].[Persona] p
            ON p.Numeross = c.NUMEROSS
        WHERE p.email = :email
          AND c.FECHAINI <= CAST(GETDATE() AS DATE)
          AND (c.FECHAFIN IS NULL OR c.FECHAFIN >= CAST(GETDATE() AS DATE))
        """)

        result = self.db.execute(sql, {"email": email})
        return [row.ceco for row in result.fetchall()]
