from app.domain.entities.cliente_proceso import ClienteProceso
from app.domain.repositories.cliente_proceso_repository import ClienteProcesoRepository
from app.infrastructure.db.models.cliente_proceso_model import ClienteProcesoModel
from app.infrastructure.mappers.cliente_proceso_mapper import mapear_modelo_a_entidad

class ClienteProcesoRepositorySQL(ClienteProcesoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, cliente_proceso: ClienteProceso):
        modelo = ClienteProcesoModel(**vars(cliente_proceso))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return mapear_modelo_a_entidad(modelo)

    def listar(self):
        return self.session.query(ClienteProcesoModel).all()

    def obtener_por_id(self, id: int):
        return self.session.query(ClienteProcesoModel).filter_by(id=id).first()

    def eliminar(self, id: int):
        instancia = self.session.query(ClienteProcesoModel).filter_by(id=id).first()
        if not instancia:
            return None
        self.session.delete(instancia)
        self.session.commit()
        return True

    def listar_por_cliente(self, idcliente: str):
        return self.session.query(ClienteProcesoModel).filter_by(idcliente=idcliente).all()
