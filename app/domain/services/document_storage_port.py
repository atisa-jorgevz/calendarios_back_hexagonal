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
    def save_with_category(self, cif: str, category_id: str, filename: str, content: bytes) -> str:
        """
        Guarda el contenido bajo una carpeta <root>/<cif>/<category_id>/ y
        devuelve el nombre de fichero generado.
        """
        pass

    @abstractmethod
    def delete(self, cif: str, stored_name: str) -> None:
        """
        Elimina el fichero <root>/<cif>/<stored_name>.
        """
        pass

    @abstractmethod
    def delete_with_category(self, cif: str, category_id: str, stored_name: str) -> None:
        """
        Elimina el fichero <root>/<cif>/<category_id>/<stored_name>.
        """
        pass

    @abstractmethod
    def get(self, cif: str, stored_name: str) -> bytes:
        """
        Obtiene el contenido del fichero <root>/<cif>/<stored_name>.
        """
        pass

    @abstractmethod
    def get_with_category(self, cif: str, category_id: str, stored_name: str) -> bytes:
        """
        Obtiene el contenido del fichero <root>/<cif>/<category_id>/<stored_name>.
        """
        pass
