from app.domain.entities.hito import Hito
from app.domain.repositories.hito_repository import HitoRepository

def crear_hito(data: dict, repo: HitoRepository):
    hito = Hito(
        nombre=data.get("nombre"),
        descripcion=data.get("descripcion"),
        frecuencia=data.get("frecuencia"),
        temporalidad=data.get("temporalidad"),
        fecha_inicio=data.get("fecha_inicio"),
        fecha_fin=data.get("fecha_fin"),
        obligatorio=data.get("obligatorio", False),
    )
    return repo.guardar(hito)
