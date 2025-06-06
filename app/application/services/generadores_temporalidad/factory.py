from .generador_mensual import GeneradorMensual
from .generador_semanal import GeneradorSemanal
from .generador_diario import GeneradorDiario
from .generador_quincenal import GeneradorQuincenal
from .generador_trimestral import GeneradorTrimestral
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
    else:
        raise ValueError(f"Temporalidad no soportada: {temporalidad}")
