class Documento:
    def __init__(self, id=None, cliente_proceso_hito_id=None, nombre_documento=None, original_file_name=None, stored_file_name=None):
        self.id = id
        self.cliente_proceso_hito_id = cliente_proceso_hito_id
        self.nombre_documento = nombre_documento
        self.original_file_name = original_file_name
        self.stored_file_name = stored_file_name
