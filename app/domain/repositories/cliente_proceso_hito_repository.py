from abc import ABC, abstractmethod
from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito

class ClienteProcesoHitoRepository(ABC):

    @abstractmethod
    def guardar(self, cliente_proceso_hito: ClienteProcesoHito):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def obtener_por_id(self, id: int):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
