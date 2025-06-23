from abc import ABC, abstractmethod
from typing import List

class ApiClienteClienteRepository(ABC):
    @abstractmethod
    def obtener_clientes_por_api_cliente(self, api_cliente_id: int) -> List[int]:
        ...
    
    @abstractmethod
    def asociar_clientes(self, api_cliente_id: int, cliente_ids: List[int]) -> None:
        ...

