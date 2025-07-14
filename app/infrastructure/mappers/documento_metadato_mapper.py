from app.domain.entities.documento_metadato import DocumentoMetadato
from app.infrastructure.db.models.documento_metadato_model import DocumentoMetadatoModel

class DocumentoMetadatoMapper:

    @staticmethod
    def to_entity(model: DocumentoMetadatoModel) -> DocumentoMetadato:
        return DocumentoMetadato(
            id=model.id,
            id_documento=model.id_documento,
            id_metadato=model.id_metadato
        )

    @staticmethod
    def to_model(entity: DocumentoMetadato) -> DocumentoMetadatoModel:
        return DocumentoMetadatoModel(
            id=entity.id,
            id_documento=entity.id_documento,
            id_metadato=entity.id_metadato
        )
