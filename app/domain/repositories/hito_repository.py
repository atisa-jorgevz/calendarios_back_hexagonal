from abc import ABC, abstractmethod
from app.domain.entities.hito import Hito

class HitoRepository(ABC):

    @abstractmethod
    def guardar(self, hito: Hito):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def obtener_por_id(self, id: int):
        pass

    @abstractmethod
    def actualizar(self, id: int, data: dict):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
    
    @abstractmethod
    def listar_hitos_cliente_por_empleado(self, email: str):
        pass
