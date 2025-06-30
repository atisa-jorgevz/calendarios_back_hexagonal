from pydantic import BaseModel
from typing import Optional

class DocumentoMetadatoCreate(BaseModel):
    id_documento: int
    id_metadato: int

class DocumentoMetadatoUpdate(DocumentoMetadatoCreate):
    id: int

class DocumentoMetadatoOut(DocumentoMetadatoUpdate):
    pass
