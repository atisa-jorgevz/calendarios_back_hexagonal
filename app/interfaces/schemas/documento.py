# app/interfaces/schemas/documento.py

from pydantic import BaseModel

class DocumentoResponse(BaseModel):
    id: int
    id_cliente_proceso_hito: int
    nombre_documento: str
    original_file_name: str
    stored_file_name: str

    class Config:
        orm_mode = True
