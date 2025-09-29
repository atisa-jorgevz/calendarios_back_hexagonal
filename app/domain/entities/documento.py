class Documento:
    def __init__(self, id=None, id_cliente_proceso_hito=None, nombre_documento=None, original_file_name=None, stored_file_name=None):
        self.id = id
        self.id_cliente_proceso_hito = id_cliente_proceso_hito
        self.nombre_documento = nombre_documento
        self.original_file_name = original_file_name
        self.stored_file_name = stored_file_name
