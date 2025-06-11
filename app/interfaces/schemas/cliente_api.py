from pydantic import BaseModel

class CrearClienteAPIRequest(BaseModel):
    nombre_cliente: str

class CambiarEstadoClienteRequest(BaseModel):
    activo: bool
