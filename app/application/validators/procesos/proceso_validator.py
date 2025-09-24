from datetime import date

def validar_datos_proceso(data: dict):
    campos_obligatorios = ["nombre", "frecuencia", "temporalidad"]
    for campo in campos_obligatorios:
        if campo not in data or data[campo] in [None, ""]:
            raise ValueError(f"El campo '{campo}' es obligatorio")

    if "frecuencia" in data and (not isinstance(data["frecuencia"], int) or data["frecuencia"] <= 0):
        raise ValueError("La frecuencia debe ser un número entero positivo")

    # Puedes seguir agregando más validaciones...
