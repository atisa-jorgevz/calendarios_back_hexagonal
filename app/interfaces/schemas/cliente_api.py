from pydantic import BaseModel
from typing import List

class CrearClienteAPIRequest(BaseModel):
    nombre_cliente: str

class CambiarEstadoClienteRequest(BaseModel):
    activo: bool

class AsociarClientesRequest(BaseModel):
    cliente_ids: List[int]
