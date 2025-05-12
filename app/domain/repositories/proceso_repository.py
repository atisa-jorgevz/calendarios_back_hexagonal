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
    def listar_procesos_y_hitos_por_empleado(        
        self, email: str
    ) -> List[Dict[str, Any]]:
         """
         Devuelve lista de dicts con la forma:
         [
           {
             "cliente": { "id": str, "nombre": str, … },
             "procesos": [
               {
                 "id": str,
                 "estado": str,
                 "fecha_creacion": datetime,
                 "hitos": [
                   { "id": str, "nombre": str, "estado": str },
                   …
                 ]
               },
               …
             ]
           },
           …
         ]
         """
