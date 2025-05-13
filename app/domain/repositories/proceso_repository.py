# app/domain/repositories/proceso_repository.py
from abc import ABC, abstractmethod
from app.domain.entities.proceso import Proceso
from typing import List, Any, Dict

class ProcesoRepository(ABC):

    @abstractmethod
    def guardar(self, proceso: Proceso):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def actualizar(self, id: int, data: dict):
        pass

    @abstractmethod
    def obtener_por_id(self, id: int):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
      
    @abstractmethod
    def listar_procesos_cliente_por_empleado(self, email: str):
        pass
