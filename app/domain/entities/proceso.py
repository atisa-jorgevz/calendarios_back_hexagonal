class Proceso:
    def __init__(self, id=None, nombre=None, frecuencia=None, temporalidad=None, descripcion=None, inicia_dia_1=False):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.frecuencia = frecuencia
        self.temporalidad = temporalidad
        self.inicia_dia_1 = inicia_dia_1
