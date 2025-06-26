from abc import ABC, abstractmethod

class DocumentStoragePort(ABC):
    @abstractmethod
    def save(self, cif: str, filename: str, content: bytes) -> str:
        """
        Guarda el contenido bajo una carpeta <root>/<cif>/ y
        devuelve el nombre de fichero generado.
        """
        pass

    @abstractmethod
    def delete(self, cif: str, stored_name: str) -> None:
        """
        Elimina el fichero <root>/<cif>/<stored_name>.
        """
        pass
