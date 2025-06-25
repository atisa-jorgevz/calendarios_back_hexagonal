from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.metadato import Metadato

class MetadatoRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Metadato]:
        pass

    @abstractmethod
    def get_by_id(self, metadato_id: int) -> Metadato | None:
        pass

    @abstractmethod
    def save(self, metadato: Metadato) -> Metadato:
        pass

    @abstractmethod
    def delete(self, metadato_id: int) -> None:
        pass

    @abstractmethod
    def update(self, metadato_id: int, metadato: Metadato) -> Metadato:
        pass

