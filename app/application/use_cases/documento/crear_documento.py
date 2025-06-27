# app/application/use_cases/documento/crear_documento.py

import os
import uuid
from app.domain.entities.documento import Documento
from app.domain.repositories.documento_repository import DocumentoRepositoryPort
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.services.document_storage_port import DocumentStoragePort

class CrearDocumentoUseCase:
    def __init__(
        self,
        documento_repo: DocumentoRepositoryPort,
        cph_repo: ClienteProcesoHitoRepository,
        cp_repo: ClienteProcesoRepository,
        cliente_repo: ClienteRepository,
        storage: DocumentStoragePort
    ):
        self.documento_repo = documento_repo
        self.cph_repo       = cph_repo
        self.cp_repo        = cp_repo
        self.cliente_repo   = cliente_repo
        self.storage        = storage

    def execute(
        self,
        id_cliente_proceso_hito: int,
        nombre_documento: str,
        original_file_name: str,
        content: bytes
    ) -> Documento:
        # 1) Recuperar ClienteProcesoHito
        cph = self.cph_repo.obtener_por_id(id_cliente_proceso_hito)
        if not cph:
            raise ValueError(f"ClienteProcesoHito {id_cliente_proceso_hito} no existe")

        # 2) Con ese cph.cliente_proceso_id, recuperar ClienteProceso
        cp = self.cp_repo.obtener_por_id(cph.cliente_proceso_id)
        if not cp:
            raise ValueError(f"ClienteProceso {cph.cliente_proceso_id} no existe")

        # 3) Con cp.idcliente, recuperar Cliente
        cliente = self.cliente_repo.obtener_por_id(cp.idcliente)
        if not cliente:
            raise ValueError(f"Cliente {cp.idcliente} no existe")

        cif = cliente.cif

        # 4) Generar nombre único manteniendo extensión
        ext = os.path.splitext(original_file_name)[1]
        stored_file_name = f"{uuid.uuid4().hex}{ext}"

        # 5) Guardar en disco bajo <ROOT>/<CIF>/
        self.storage.save(cif, stored_file_name, content)

        # 6) Construir entidad y persistir en BD
        nuevo_doc = Documento(
            id=None,
            id_cliente_proceso_hito=id_cliente_proceso_hito,
            nombre_documento=nombre_documento,
            original_file_name=original_file_name,
            stored_file_name=stored_file_name
        )
        return self.documento_repo.create(nuevo_doc)
