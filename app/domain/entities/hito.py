from datetime import date, time

class Hito:
    def __init__(self,id = None, nombre: str = None , frecuencia: int = None , temporalidad: str = None, fecha_inicio: date = None, fecha_fin: date = None, hora_limite: time = None, descripcion: str = None, obligatorio: bool = False, tipo: str = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.frecuencia = frecuencia
        self.temporalidad = temporalidad
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.hora_limite = hora_limite
        self.obligatorio = obligatorio
        self.tipo = tipo
