from .generador_mensual import GeneradorMensual
from .generador_semanal import GeneradorSemanal
from .generador_diario import GeneradorDiario
from .generador_quincenal import GeneradorQuincenal
from .generador_trimestral import GeneradorTrimestral
from .generador_semestral import GeneradorSemestral
from .base_generador import GeneradorTemporalidad

def obtener_generador(temporalidad: str) -> GeneradorTemporalidad:
    temporalidad = temporalidad.lower()
    if temporalidad == "mes":
        return GeneradorMensual()
    elif temporalidad == "semana":
        return GeneradorSemanal()
    elif temporalidad == "dia":
        return GeneradorDiario()
    elif temporalidad == "quincena":
        return GeneradorQuincenal()
    elif temporalidad == "trimestre":
        return GeneradorTrimestral()
    elif temporalidad == "semestre":
        return GeneradorSemestral()
    else:
        raise ValueError(f"Temporalidad no soportada: {temporalidad}")
