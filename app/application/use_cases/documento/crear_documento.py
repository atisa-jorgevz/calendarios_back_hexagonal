from app.domain.entities.documento import Documento
from app.domain.repositories.documento_repository import DocumentoRepository
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository

class CrearDocumentoUseCase:
    def __init__(
        self,
        documento_repo: DocumentoRepository,
        cliente_proceso_hito_repo: ClienteProcesoHitoRepository
    ):
        self.documento_repo = documento_repo
        self.cliente_proceso_hito_repo = cliente_proceso_hito_repo

    def execute(self, id_cliente_proceso_hito: int, nombre_documento: str) -> Documento:
        if not self.cliente_proceso_hito_repo.get_by_id(id_cliente_proceso_hito):
            raise ValueError("El cliente_proceso_hito no existe")

        doc = Documento(
            id=None,
            id_cliente_proceso_hito=id_cliente_proceso_hito,
            nombre_documento=nombre_documento
        )
        return self.documento_repo.save(doc)
