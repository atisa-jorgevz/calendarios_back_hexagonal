from typing import List
from app.domain.repositories.api_cliente_cliente_repository import ApiClienteClienteRepository

class AsociarClientesApiCliente:
    def __init__(self, repo: ApiClienteClienteRepository):
        self.repo = repo

    def execute(self, api_cliente_id: int, cliente_ids: List[int]) -> None:
        self.repo.asociar_clientes(api_cliente_id, cliente_ids)
