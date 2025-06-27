from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentoMetadato:
    id: int | None
    id_documento: int
    id_metadato: int
