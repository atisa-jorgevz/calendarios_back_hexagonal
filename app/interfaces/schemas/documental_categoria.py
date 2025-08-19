from pydantic import BaseModel
from typing import Optional

class DocumentalCategoriaCreate(BaseModel):
    id_cliente: str
    nombre: str

class DocumentalCategoriaUpdate(BaseModel):
    nombre: Optional[str] = None

class DocumentalCategoriaResponse(BaseModel):
    id: int
    id_cliente: str
    nombre: str

    class Config:
        orm_mode = True
