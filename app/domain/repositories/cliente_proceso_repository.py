from abc import ABC, abstractmethod
from app.domain.entities.cliente_proceso import ClienteProceso

class ClienteProcesoRepository(ABC):

    @abstractmethod
    def guardar(self, cliente_proceso: ClienteProceso):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_por_cliente(self, id_cliente: int):
        pass

    @abstractmethod
    def obtener_por_id(self, id: int):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
