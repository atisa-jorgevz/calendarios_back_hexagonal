# app/application/use_cases/documental_documentos/crear_documento_categoria.py

import os
import uuid
from app.domain.entities.documental_documentos import DocumentalDocumentos
from app.domain.repositories.documental_documentos_repository import DocumentalDocumentosRepository
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.services.document_storage_port import DocumentStoragePort

class CrearDocumentoCategoriaUseCase:
    def __init__(
        self,
        documento_repo: DocumentalDocumentosRepository,
        cliente_repo: ClienteRepository,
        storage: DocumentStoragePort
    ):
        self.documento_repo = documento_repo
        self.cliente_repo = cliente_repo
        self.storage = storage

    def execute(
        self,
        id_cliente: str,
        id_categoria: int,
        nombre_documento: str,
        original_file_name: str,
        content: bytes
    ) -> DocumentalDocumentos:
        # 1) Verificar que el cliente existe
        cliente = self.cliente_repo.obtener_por_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} no existe")

        cif = cliente.cif

        # 2) Generar nombre único manteniendo extensión
        ext = os.path.splitext(original_file_name)[1]
        stored_file_name = f"{uuid.uuid4().hex}{ext}"

        # 3) Guardar en disco bajo <ROOT>/<CIF>/<ID_CATEGORIA>/
        # Usamos el método save_with_category del storage
        self.storage.save_with_category(cif, str(id_categoria), stored_file_name, content)

        # 4) Construir entidad y persistir en BD
        nuevo_doc = DocumentalDocumentos(
            id=None,
            id_cliente=id_cliente,
            id_categoria=id_categoria,
            nombre_documento=nombre_documento,
            original_file_name=original_file_name,
            stored_file_name=stored_file_name
        )

        return self.documento_repo.guardar(nuevo_doc)
