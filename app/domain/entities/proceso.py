class Proceso:
    def __init__(self, id=None, nombre=None, frecuencia=None, temporalidad=None, descripcion=None, fecha_inicio=None, fecha_fin=None, inicia_dia_1=False):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.frecuencia = frecuencia
        self.temporalidad = temporalidad
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.inicia_dia_1 = inicia_dia_1

