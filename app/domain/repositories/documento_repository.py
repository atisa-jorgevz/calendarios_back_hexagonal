from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.documento import Documento

class DocumentoRepositoryPort(ABC):
    @abstractmethod
    def create(self, doc: Documento) -> Documento:
        pass

    @abstractmethod
    def update(self, doc: Documento) -> Documento:
        pass

    @abstractmethod
    def delete(self, doc_id: int) -> None:
        pass

    @abstractmethod
    def get_by_id(self, doc_id: int) -> Documento | None:
        pass

    @abstractmethod
    def get_all(self) -> List[Documento]: pass
