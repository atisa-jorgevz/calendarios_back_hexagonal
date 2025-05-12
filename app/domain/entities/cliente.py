from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    idcliente: str
    cif: Optional[str]
    cif_empresa: Optional[str]
    razsoc: Optional[str]
    direccion: Optional[str]
    localidad: Optional[str]
    provincia: Optional[str]
    cpostal: Optional[str]
    codigop: Optional[str]
    pais: Optional[str]
    cif_factura: Optional[str]
