from pydantic import BaseModel
from datetime import date
from typing import Optional

class GenerarClienteProcesoRequest(BaseModel):
    idcliente: int
    id_proceso: int
    fecha_inicio: Optional[date] = None
