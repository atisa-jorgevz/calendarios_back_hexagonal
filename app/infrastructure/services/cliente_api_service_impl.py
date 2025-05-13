from app.domain.services.cliente_api_service import ClienteAPIService
from app.infrastructure.db.models.api_cliente_model import ApiClienteModel

class ClienteAPIServiceImpl(ClienteAPIService):
    def __init__(self, session):
        self.session = session

    def validar_api_key(self, clave: str) -> bool:
        cliente = (
            self.session.query(ApiClienteModel)
            .filter_by(api_key=clave, activo=True)
            .first()
        )
        return cliente is not None
