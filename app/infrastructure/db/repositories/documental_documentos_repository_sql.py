from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.repositories.documental_documentos_repository import DocumentalDocumentosRepository
from app.domain.entities.documental_documentos import DocumentalDocumentos
from app.infrastructure.db.models.documental_documentos_model import DocumentalDocumentosModel

class SqlDocumentalDocumentosRepository(DocumentalDocumentosRepository):
    def __init__(self, session: Session):
        self.session = session

    def _mapear_modelo_a_entidad(self, modelo: DocumentalDocumentosModel) -> DocumentalDocumentos:
        """Convierte un modelo SQLAlchemy a una entidad del dominio"""
        return DocumentalDocumentos(
            id=modelo.id,
            id_cliente=modelo.id_cliente,
            id_categoria=modelo.id_categoria,
            nombre_documento=modelo.nombre_documento,
            original_file_name=modelo.original_file_name,
            stored_file_name=modelo.stored_file_name
        )

    def guardar(self, documento_documentos: DocumentalDocumentos) -> DocumentalDocumentos:
        # Excluir el id si es None para que se auto-genere
        data = {k: v for k, v in vars(documento_documentos).items() if v is not None}
        modelo = DocumentalDocumentosModel(**data)
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return self._mapear_modelo_a_entidad(modelo)

    def actualizar(self, id: int, data: dict) -> DocumentalDocumentos | None:
        documento_documentos = self.session.query(DocumentalDocumentosModel).filter_by(id=id).first()
        if not documento_documentos:
            return None

        for key, value in data.items():
            setattr(documento_documentos, key, value)

        self.session.commit()
        self.session.refresh(documento_documentos)
        return self._mapear_modelo_a_entidad(documento_documentos)

    def listar(self) -> List[DocumentalDocumentos]:
        modelos = self.session.query(DocumentalDocumentosModel).all()
        return [self._mapear_modelo_a_entidad(modelo) for modelo in modelos]

    def obtener_por_id(self, id: int) -> DocumentalDocumentos | None:
        modelo = self.session.query(DocumentalDocumentosModel).filter_by(id=id).first()
        if not modelo:
            return None
        return self._mapear_modelo_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        documento_documentos = self.session.query(DocumentalDocumentosModel).filter_by(id=id).first()
        if not documento_documentos:
            return False
        self.session.delete(documento_documentos)
        self.session.commit()
        return True

    def obtener_por_cliente_categoria(self, id_cliente: str, id_categoria: int) -> List[DocumentalDocumentos]:
        modelos = self.session.query(DocumentalDocumentosModel).filter_by(
            id_cliente=id_cliente,
            id_categoria=id_categoria
        ).all()
        return [self._mapear_modelo_a_entidad(modelo) for modelo in modelos]
