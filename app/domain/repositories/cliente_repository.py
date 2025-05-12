from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.cliente import Cliente

class ClienteRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Cliente]:
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        pass

    @abstractmethod
    def buscar_por_cif(self, cif: str) -> Optional[Cliente]:
        pass
