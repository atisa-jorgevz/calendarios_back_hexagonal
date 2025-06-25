from pydantic import BaseModel

class DocumentoCreate(BaseModel):
    id_cliente_proceso_hito: int
    nombre_documento: str

class DocumentoRead(DocumentoCreate):
    id: int

    class Config:
        orm_mode = True
