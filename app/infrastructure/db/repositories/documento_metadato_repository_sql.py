from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.documento_metadato import DocumentoMetadato
from app.domain.repositories.documento_metadato_repository import DocumentoMetadatoRepository
from app.infrastructure.db.models.documento_metadato_model import DocumentoMetadatoModel
from app.infrastructure.mappers.documento_metadato_mapper import DocumentoMetadatoMapper

class SqlDocumentoMetadatoRepository(DocumentoMetadatoRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def crear(self, doc_metadato: DocumentoMetadato) -> DocumentoMetadato:
        model = DocumentoMetadatoMapper.to_model(doc_metadato)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return DocumentoMetadatoMapper.to_entity(model)

    def actualizar(self, doc_metadato: DocumentoMetadato) -> DocumentoMetadato:
        model = self.db.query(DocumentoMetadatoModel).get(doc_metadato.id)
        model.id_documento = doc_metadato.id_documento
        model.id_metadato = doc_metadato.id_metadato
        self.db.commit()
        self.db.refresh(model)
        return DocumentoMetadatoMapper.to_entity(model)

    def eliminar(self, id: int) -> None:
        self.db.query(DocumentoMetadatoModel).filter_by(id=id).delete()
        self.db.commit()

    def obtener_por_id(self, id: int) -> DocumentoMetadato | None:
        model = self.db.query(DocumentoMetadatoModel).get(id)
        return DocumentoMetadatoMapper.to_entity(model) if model else None

    def obtener_por_documento(self, id_documento: int) -> List[DocumentoMetadato]:
        rows = self.db.query(DocumentoMetadatoModel).filter_by(id_documento=id_documento).all()
        return [DocumentoMetadatoMapper.to_entity(r) for r in rows]

    def listar_todos(self) -> List[DocumentoMetadato]:
        rows = self.db.query(DocumentoMetadatoModel).all()
        return [DocumentoMetadatoMapper.to_entity(r) for r in rows]
