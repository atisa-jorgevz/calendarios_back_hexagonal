from abc import ABC, abstractmethod
from app.domain.entities.proceso import Proceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository

class GeneradorTemporalidad(ABC):
    @abstractmethod
    def generar(self, data, proceso_maestro: Proceso, repo: ClienteProcesoRepository) -> dict:
        pass
