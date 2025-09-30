# app/infrastructure/db/repositories/documento_repository_sql.py

from sqlalchemy.orm import Session
from typing import List

from app.domain.entities.documento import Documento
from app.domain.repositories.documento_repository import DocumentoRepositoryPort
from app.infrastructure.db.models.documento_model import DocumentoModel

class SQLDocumentoRepository(DocumentoRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Documento]:
        modelos = self.session.query(DocumentoModel).all()
        return [self._to_entity(m) for m in modelos]

    def get_by_id(self, doc_id: int) -> Documento | None:
        m = (
            self.session
            .query(DocumentoModel)
            .filter_by(id=doc_id)
            .first()
        )
        return self._to_entity(m) if m else None

    def create(self, doc: Documento) -> Documento:
        modelo = DocumentoModel(
            cliente_proceso_hito_id=doc.cliente_proceso_hito_id,
            nombre_documento        = doc.nombre_documento,
            original_file_name        = doc.original_file_name,
            stored_file_name          = doc.stored_file_name
        )
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return self._to_entity(modelo)

    def update(self, doc: Documento) -> Documento:
        modelo = (
            self.session
            .query(DocumentoModel)
            .filter_by(id=doc.id)
            .first()
        )
        if not modelo:
            raise ValueError(f"Documento {doc.id} no existe")
        # Actualizamos ambos campos de nombre
        modelo.nombre_documento    = doc.nombre_documento
        modelo.original_file_name = doc.original_file_name
        modelo.stored_file_name   = doc.stored_file_name
        self.session.commit()
        self.session.refresh(modelo)
        return self._to_entity(modelo)

    def delete(self, doc_id: int) -> None:
        (
            self.session
            .query(DocumentoModel)
            .filter_by(id=doc_id)
            .delete()
        )
        self.session.commit()

    def _to_entity(self, m: DocumentoModel) -> Documento:
        return Documento(
            id                         = m.id,
            cliente_proceso_hito_id    = m.cliente_proceso_hito_id,
            nombre_documento           = m.nombre_documento,
            original_file_name         = m.original_file_name,
            stored_file_name           = m.stored_file_name
        )
