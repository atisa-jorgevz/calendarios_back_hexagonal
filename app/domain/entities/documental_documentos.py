from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentalDocumentos:
    id: int
    id_cliente: str
    id_categoria: int
    nombre_documento: str
    original_file_name: str
    stored_file_name: str
