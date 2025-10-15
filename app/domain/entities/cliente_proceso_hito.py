class ClienteProcesoHito:
    def __init__(self, id=None, cliente_proceso_id=None, hito_id=None, estado=None, fecha_estado=None, fecha_limite=None, hora_limite=None, tipo=None, habilitado=True):
        self.id = id
        self.cliente_proceso_id = cliente_proceso_id
        self.hito_id = hito_id
        self.estado = estado
        self.fecha_estado = fecha_estado
        self.fecha_limite = fecha_limite
        self.hora_limite = hora_limite
        self.tipo = tipo
        self.habilitado = habilitado
