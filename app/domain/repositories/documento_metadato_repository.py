from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.documento_metadato import DocumentoMetadato

class DocumentoMetadatoRepository(ABC):

    @abstractmethod
    def crear(self, doc_metadato: DocumentoMetadato) -> DocumentoMetadato:
        pass

    @abstractmethod
    def actualizar(self, doc_metadato: DocumentoMetadato) -> DocumentoMetadato:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> DocumentoMetadato | None:
        pass

    @abstractmethod
    def obtener_por_documento(self, id_documento: int) -> List[DocumentoMetadato]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[DocumentoMetadato]:
        pass
