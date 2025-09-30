from pydantic import BaseModel
from datetime import date
from typing import Optional

class GenerarClienteProcesoRequest(BaseModel):
    cliente_id: str
    proceso_id: int
    fecha_inicio: Optional[date] = None
