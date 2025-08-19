from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentalCategoria:
    id: int
    id_cliente: str
    nombre: str
