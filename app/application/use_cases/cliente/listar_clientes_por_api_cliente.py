from typing import List
from app.domain.repositories.api_cliente_cliente_repository import ApiClienteClienteRepository
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.entities.cliente import Cliente

class ListarClientesPorApiCliente:
    def __init__(
        self,
        api_cliente_cliente_repo: ApiClienteClienteRepository,
        cliente_repo: ClienteRepository
    ):
        self.api_cliente_cliente_repo = api_cliente_cliente_repo
        self.cliente_repo = cliente_repo

    def execute(self, api_cliente_id: int) -> List[Cliente]:
        ids_clientes = self.api_cliente_cliente_repo.obtener_clientes_por_api_cliente(api_cliente_id)
        return self.cliente_repo.obtener_clientes_por_ids(ids_clientes)
