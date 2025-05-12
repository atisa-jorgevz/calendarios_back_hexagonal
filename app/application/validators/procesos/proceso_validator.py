from datetime import date

def validar_datos_proceso(data: dict):
    campos_obligatorios = ["nombre", "frecuencia", "temporalidad", "fecha_inicio"]
    for campo in campos_obligatorios:
        if campo not in data or data[campo] in [None, ""]:
            raise ValueError(f"El campo '{campo}' es obligatorio")

    if "frecuencia" in data and (not isinstance(data["frecuencia"], int) or data["frecuencia"] <= 0):
        raise ValueError("La frecuencia debe ser un número entero positivo")

    if "fecha_inicio" in data:
        try:
            date.fromisoformat(data["fecha_inicio"])
        except ValueError:
            raise ValueError("La fecha_inicio debe tener formato YYYY-MM-DD")

    # Puedes seguir agregando más validaciones...
