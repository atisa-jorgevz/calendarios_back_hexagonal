from sqlalchemy.orm import Session
from typing import List
from app.domain.entities.documento import Documento
from app.domain.repositories.documento_repository import DocumentoRepository
from app.infrastructure.db.models.documento_model import DocumentoModel

class SQLDocumentoRepository(DocumentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Documento]:
        return [self._to_entity(d) for d in self.session.query(DocumentoModel).all()]

    def get_by_id(self, id: int) -> Documento | None:
        d = self.session.query(DocumentoModel).filter_by(id=id).first()
        return self._to_entity(d) if d else None

    def save(self, doc: Documento) -> Documento:
        modelo = DocumentoModel(
            id_cliente_proceso_hito=doc.id_cliente_proceso_hito,
            nombre_documento=doc.nombre_documento
        )
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return self._to_entity(modelo)

    def delete(self, id: int) -> None:
        self.session.query(DocumentoModel).filter_by(id=id).delete()
        self.session.commit()

    def _to_entity(self, m: DocumentoModel) -> Documento:
        return Documento(
            id=m.id,
            id_cliente_proceso_hito=m.id_cliente_proceso_hito,
            nombre_documento=m.nombre_documento
        )
