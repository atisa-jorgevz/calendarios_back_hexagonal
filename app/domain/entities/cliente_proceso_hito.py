class ClienteProcesoHito:
    def __init__(self, id, cliente_proceso_id, hito_id, estado, fecha_inicio, fecha_fin=None,fecha_estado=None):
        self.id = id
        self.cliente_proceso_id = cliente_proceso_id
        self.hito_id = hito_id
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.fecha_estado = fecha_estado
        
