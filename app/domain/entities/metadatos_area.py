from dataclasses import dataclass

@dataclass(frozen=True)
class MetadatosArea:
    id: int | None
    id_metadato: int
    codigo_ceco: str
