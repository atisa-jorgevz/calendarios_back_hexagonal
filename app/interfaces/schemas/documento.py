# app/interfaces/schemas/documento.py

from pydantic import BaseModel

class DocumentoResponse(BaseModel):
    id: int
    cliente_proceso_hito_id: int
    nombre_documento: str
    original_file_name: str
    stored_file_name: str

    class Config:
        orm_mode = True
