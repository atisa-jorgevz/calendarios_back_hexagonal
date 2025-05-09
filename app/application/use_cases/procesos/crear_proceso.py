from app.domain.entities.proceso import Proceso
from app.domain.repositories.proceso_repository import ProcesoRepository

def crear_proceso(data: dict,proceso_repository: ProcesoRepository):
    proceso = Proceso(
        nombre=data["nombre"],
        descripcion=data.get("descripcion"),
        frecuencia=data["frecuencia"],
        temporalidad=data["temporalidad"],
        fecha_inicio=data.get("fecha_inicio"),
        fecha_fin=data.get("fecha_fin"),
        inicia_dia_1=data.get("inicia_dia_1", False)
    )
    return proceso_repository.guardar(proceso)
