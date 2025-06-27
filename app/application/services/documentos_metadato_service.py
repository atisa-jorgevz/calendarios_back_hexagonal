from typing import List
from fastapi import HTTPException
from app.domain.entities.documento_metadato import DocumentoMetadato
from app.domain.repositories.documento_metadato_repository import DocumentoMetadatoRepository
from app.domain.repositories.documento_repository import DocumentoRepositoryPort
from app.domain.repositories.metadato_repository import MetadatoRepository

class DocumentoMetadatoService:
    def __init__(
        self,
        repo: DocumentoMetadatoRepository,
        doc_repo: DocumentoRepositoryPort,
        meta_repo: MetadatoRepository
    ):
        self.repo = repo
        self.doc_repo = doc_repo
        self.meta_repo = meta_repo

    def _validar_referencias(self, doc: DocumentoMetadato):
        if not self.doc_repo.get_by_id(doc.id_documento):
            raise HTTPException(status_code=400, detail="Documento no existe")
        if not self.meta_repo.get_by_id(doc.id_metadato):
            raise HTTPException(status_code=400, detail="Metadato no existe")

    def crear(self, doc: DocumentoMetadato) -> DocumentoMetadato:
        self._validar_referencias(doc)
        return self.repo.crear(doc)

    def actualizar(self, doc: DocumentoMetadato) -> DocumentoMetadato:
        self._validar_referencias(doc)
        return self.repo.actualizar(doc)

    def eliminar(self, id: int) -> None:
        obj = self.repo.obtener_por_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="DocumentoMetadato no existe")
        self.repo.eliminar(id)

    def obtener_por_id(self, id: int) -> DocumentoMetadato | None:
        return self.repo.obtener_por_id(id)

    def listar(self) -> List[DocumentoMetadato]:
        return self.repo.listar_todos()
