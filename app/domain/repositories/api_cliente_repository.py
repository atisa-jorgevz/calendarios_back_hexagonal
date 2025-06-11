from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.api_cliente import ApiCliente

class ApiClienteRepository(ABC):
    @abstractmethod
    def get_by_nombre(self, nombre_cliente: str) -> Optional[ApiCliente]:
        pass
