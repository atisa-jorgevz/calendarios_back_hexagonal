from sqlalchemy.orm import Session
from app.domain.repositories.api_cliente_cliente_repository import ApiClienteClienteRepository
from app.infrastructure.db.models.api_cliente_cliente_model import ApiClienteClienteModel
from typing import List

class SqlApiClienteClienteRepository(ApiClienteClienteRepository):
    def __init__(self, session: Session):
        self.session = session

    def obtener_clientes_por_api_cliente(self, api_cliente_id: int):
        result = self.session.query(ApiClienteClienteModel.cliente_id).filter_by(api_cliente_id=api_cliente_id).all()
        return [row.cliente_id for row in result]

    def asociar_clientes(self, api_cliente_id: int, cliente_ids: List[int]) -> None:
        self.session.query(ApiClienteClienteModel).filter_by(api_cliente_id=api_cliente_id).delete()
        self.session.bulk_save_objects([
            ApiClienteClienteModel(api_cliente_id=api_cliente_id, cliente_id=cid)
            for cid in cliente_ids
        ])
        self.session.commit()

