from app.domain.entities.proceso import Proceso
from app.domain.repositories.proceso_repository import ProcesoRepository
from app.application.validators.procesos.proceso_validator import validar_datos_proceso

def crear_proceso(data: dict,proceso_repository: ProcesoRepository):

    validar_datos_proceso(data)  # 💥 Si hay error, lanza excepción

    proceso = Proceso(
        nombre=data["nombre"],
        descripcion=data.get("descripcion"),
        frecuencia=data["frecuencia"],
        temporalidad=data["temporalidad"],
        inicia_dia_1=data.get("inicia_dia_1", False)
    )
    return proceso_repository.guardar(proceso)
