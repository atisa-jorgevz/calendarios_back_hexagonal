from dataclasses import dataclass

@dataclass(frozen=True)
class Documento:
    id: int | None
    id_cliente_proceso_hito: int
    nombre_documento: str
