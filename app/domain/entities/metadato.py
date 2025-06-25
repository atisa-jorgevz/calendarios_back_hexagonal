from dataclasses import dataclass


@dataclass(frozen=True)
class Metadato:
    id: int | None
    nombre: str
    descripcion: str
    tipo_generacion: str
    global_: int
    activo: int
