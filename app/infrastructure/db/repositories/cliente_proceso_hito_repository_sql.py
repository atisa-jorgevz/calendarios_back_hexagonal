# app/infrastructure/db/repositories/cliente_proceso_hito_repository_sql.py

from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.infrastructure.db.models.cliente_proceso_hito_model import ClienteProcesoHitoModel

class ClienteProcesoHitoRepositorySQL(ClienteProcesoHitoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, relacion: ClienteProcesoHito):
        modelo = ClienteProcesoHitoModel(**vars(relacion))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def listar(self):
        return self.session.query(ClienteProcesoHitoModel).all()

    def obtener_por_id(self, id: int):
        return self.session.query(ClienteProcesoHitoModel).filter_by(id=id).first()

    def eliminar(self, id: int):
        relacion = self.obtener_por_id(id)
        if not relacion:
            return False
        self.session.delete(relacion)
        self.session.commit()
        return True

    def obtener_por_cliente_proceso_id(self, cliente_proceso_id: int):
        return self.session.query(ClienteProcesoHitoModel).filter_by(cliente_proceso_id=cliente_proceso_id).all()
