from app.domain.repositories.documento_repository import DocumentoRepositoryPort
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.services.document_storage_port import DocumentStoragePort

class EliminarDocumentoUseCase:
    def __init__(
        self,
        documento_repo: DocumentoRepositoryPort,
        cph_repo: ClienteProcesoHitoRepository,
        storage: DocumentStoragePort
    ):
        self.documento_repo = documento_repo
        self.cph_repo       = cph_repo
        self.storage        = storage

    def execute(self, id_documento: int) -> None:
        # 1) Recuperar registro
        doc = self.documento_repo.get_by_id(id_documento)
        if not doc:
            raise ValueError(f"Documento {id_documento} no existe")

        # 2) Obtener CIF
        relacion = self.cph_repo.obtener_por_id(doc.cliente_proceso_hito_id)
        if not relacion:
            raise ValueError(f"ClienteProcesoHito {doc.cliente_proceso_hito_id} no encontrado")
        cif = relacion.cliente_proceso.cliente.cif

        # 3) Borrar fichero físico
        self.storage.delete(cif, doc.nombre_documento_almacenado)

        # 4) Borrar registro en BD
        self.documento_repo.delete(id_documento)
