from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.documento import Documento

class DocumentoRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Documento]: pass

    @abstractmethod
    def get_by_id(self, id: int) -> Documento | None: pass

    @abstractmethod
    def save(self, documento: Documento) -> Documento: pass

    @abstractmethod
    def delete(self, id: int) -> None: pass
