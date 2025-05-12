class ClienteProceso:
    def __init__(self, id, idcliente, id_proceso, fecha_inicio, fecha_fin=None, mes=None, anio=None, id_anterior=None):
        self.id = id
        self.idcliente = idcliente
        self.id_proceso = id_proceso
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.mes = mes
        self.anio = anio
        self.id_anterior = id_anterior
