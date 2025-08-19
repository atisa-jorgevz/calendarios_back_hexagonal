import os
from app.domain.services.document_storage_port import DocumentStoragePort
from app.config import settings

class LocalFileStorage(DocumentStoragePort):
    def __init__(self):
        self.root = settings.FILE_STORAGE_ROOT

    def save(self, cif: str, filename: str, content: bytes) -> str:
        if not content or len(content) == 0:
            raise ValueError("No se puede guardar un archivo vacío")

        cif = cif.strip()
        dir_path = os.path.join(self.root, cif)

        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # Verificar que el archivo se guardó correctamente
        if not os.path.exists(file_path) or os.path.getsize(file_path) != len(content):
            raise IOError("Error al guardar archivo: verificación fallida")

        return filename

    def save_with_category(self, cif: str, category_id: str, filename: str, content: bytes) -> str:
        if not content or len(content) == 0:
            raise ValueError("No se puede guardar un archivo vacío")

        cif = cif.strip()
        category_id = str(category_id).strip()
        dir_path = os.path.join(self.root, cif, category_id)

        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # Verificar que el archivo se guardó correctamente
        if not os.path.exists(file_path) or os.path.getsize(file_path) != len(content):
            raise IOError("Error al guardar archivo: verificación fallida")

        return filename

    def delete(self, cif: str, stored_name: str) -> None:
        cif = cif.strip()
        file_path = os.path.join(self.root, cif, stored_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def delete_with_category(self, cif: str, category_id: str, stored_name: str) -> None:
        cif = cif.strip()
        category_id = str(category_id).strip()
        file_path = os.path.join(self.root, cif, category_id, stored_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get(self, cif: str, stored_name: str) -> bytes:
        cif = cif.strip()
        file_path = os.path.join(self.root, cif, stored_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        # Verificar que el archivo no esté vacío
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise IOError(f"Archivo vacío: {file_path}")

        with open(file_path, "rb") as f:
            content = f.read()

        # Verificar que se leyó todo el contenido
        if len(content) != file_size:
            raise IOError(f"Error al leer archivo: contenido incompleto")

        return content

    def get_with_category(self, cif: str, category_id: str, stored_name: str) -> bytes:
        cif = cif.strip()
        category_id = str(category_id).strip()
        file_path = os.path.join(self.root, cif, category_id, stored_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        # Verificar que el archivo no esté vacío
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise IOError(f"Archivo vacío: {file_path}")

        with open(file_path, "rb") as f:
            content = f.read()

        # Verificar que se leyó todo el contenido
        if len(content) != file_size:
            raise IOError(f"Error al leer archivo: contenido incompleto")

        return content
