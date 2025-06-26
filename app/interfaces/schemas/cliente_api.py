from pydantic import BaseModel
from typing import List, Optional

class CrearClienteAPIRequest(BaseModel):
    nombre_cliente: str
    password: Optional[str] = None

class CambiarEstadoClienteRequest(BaseModel):
    activo: bool

class AsociarClientesRequest(BaseModel):
    cliente_ids: List[int]

class ValidarPasswordRequest(BaseModel):
    password: str
