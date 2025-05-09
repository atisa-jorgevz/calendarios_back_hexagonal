from abc import ABC, abstractmethod
from app.domain.entities.proceso_hito_maestro import ProcesoHitoMaestro

class ProcesoHitoMaestroRepository(ABC):

    @abstractmethod
    def guardar(self, relacion: ProcesoHitoMaestro):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def eliminar(self):
        pass

    @abstractmethod
    def obtener_por_id(self):
        pass

    
