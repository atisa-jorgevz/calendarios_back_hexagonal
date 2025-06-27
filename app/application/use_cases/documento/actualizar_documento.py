# app/application/use_cases/documento/actualizar_documento.py

import os
import uuid
from app.domain.entities.documento import Documento
from app.domain.repositories.documento_repository import DocumentoRepositoryPort
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.services.document_storage_port import DocumentStoragePort

class ActualizarDocumentoUseCase:
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
        id_documento: int,
        nuevo_nombre_documento: str | None = None,   # ← ahora opcional
        nuevo_original_file_name: str | None = None,
        nuevo_content: bytes | None        = None
    ) -> Documento:
        existente = self.documento_repo.get_by_id(id_documento)
        if not existente:
            raise ValueError(f"Documento {id_documento} no existe")

        # 1) Mismo flujo para sacar cif
        cph = self.cph_repo.obtener_por_id(existente.id_cliente_proceso_hito)
        if not cph:
            raise ValueError(...)
        cp = self.cp_repo.obtener_por_id(cph.cliente_proceso_id)
        if not cp:
            raise ValueError(...)
        cliente = self.cliente_repo.obtener_por_id(cp.idcliente)
        if not cliente:
            raise ValueError(...)
        cif = cliente.cif

        # 2) Si actualizamos fichero
        if nuevo_content is not None and nuevo_original_file_name:
            # borrar viejo
            self.storage.delete(cif, existente.stored_file_name)
            # guardar nuevo
            ext = os.path.splitext(nuevo_original_file_name)[1]
            nuevo_stored = f"{uuid.uuid4().hex}{ext}"
            self.storage.save(cif, nuevo_stored, nuevo_content)
            existente.original_file_name = nuevo_original_file_name
            existente.stored_file_name   = nuevo_stored

        # 3) Si actualizamos nombre de documento
        if nuevo_nombre_documento is not None:
            existente.nombre_documento = nuevo_nombre_documento

        return self.documento_repo.update(existente)
