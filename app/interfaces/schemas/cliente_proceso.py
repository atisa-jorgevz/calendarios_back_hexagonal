from pydantic import BaseModel
from datetime import date

class GenerarClienteProcesoRequest(BaseModel):
    idcliente: int
    id_proceso: int
    fecha_inicio: date
