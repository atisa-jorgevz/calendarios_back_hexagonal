class ClienteProcesoHito:
    def __init__(self, id, cliente_proceso_id, hito_id, estado, fecha_estado=None):
        self.id = id
        self.cliente_proceso_id = cliente_proceso_id
        self.hito_id = hito_id
        self.estado = estado
        self.fecha_estado = fecha_estado
