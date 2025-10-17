# app/domain/repositories/proceso_repository.py
from abc import ABC, abstractmethod
from app.domain.entities.proceso import Proceso
from typing import List, Any, Dict, Optional

class ProcesoRepository(ABC):

    @abstractmethod
    def guardar(self, proceso: Proceso):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_habilitados(self):
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
    def listar_procesos_cliente_por_empleado(self,
        email: str,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        mes: Optional[int] = None,
        anio: Optional[int] = None
    ):
        pass
