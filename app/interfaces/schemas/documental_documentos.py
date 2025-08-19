from pydantic import BaseModel
from typing import Optional

class DocumentalDocumentosCreate(BaseModel):
    id_cliente: str
    id_categoria: int
    nombre_documento: str
    original_file_name: str
    stored_file_name: str

class DocumentalDocumentosUpdate(BaseModel):
    id_cliente: Optional[str] = None
    id_categoria: Optional[int] = None
    nombre_documento: Optional[str] = None
    original_file_name: Optional[str] = None
    stored_file_name: Optional[str] = None

class DocumentalDocumentosResponse(BaseModel):
    id: int
    id_cliente: str
    id_categoria: int
    nombre_documento: str
    original_file_name: str
    stored_file_name: str

    class Config:
        orm_mode = True
