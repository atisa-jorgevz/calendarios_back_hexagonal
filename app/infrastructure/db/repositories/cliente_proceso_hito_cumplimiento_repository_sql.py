# app/infrastructure/db/repositories/cliente_proceso_hito_cumplimiento_repository_sql.py

from app.domain.entities.cliente_proceso_hito_cumplimiento import ClienteProcesoHitoCumplimiento
from app.domain.repositories.cliente_proceso_hito_cumplimiento_repository import ClienteProcesoHitoCumplimientoRepository
from app.infrastructure.db.models.cliente_proceso_hito_cumplimiento_model import ClienteProcesoHitoCumplimientoModel

class ClienteProcesoHitoCumplimientoRepositorySQL(ClienteProcesoHitoCumplimientoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, cliente_proceso_hito_cumplimiento: ClienteProcesoHitoCumplimiento):
        # Obtener todos los atributos de la entidad
        datos = vars(cliente_proceso_hito_cumplimiento)

        # Filtrar el campo 'id' si es None para evitar problemas con SQLAlchemy
        if datos.get('id') is None:
            datos.pop('id', None)

        modelo = ClienteProcesoHitoCumplimientoModel(**datos)
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def listar(self):
        modelos = self.session.query(ClienteProcesoHitoCumplimientoModel).all()
        return modelos

    def obtener_por_id(self, id: int):
        modelo = self.session.query(ClienteProcesoHitoCumplimientoModel).filter(
            ClienteProcesoHitoCumplimientoModel.id == id
        ).first()
        return modelo

    def actualizar(self, id: int, data: dict):
        modelo = self.session.query(ClienteProcesoHitoCumplimientoModel).filter(
            ClienteProcesoHitoCumplimientoModel.id == id
        ).first()

        if not modelo:
            return None

        # Actualizar los campos proporcionados
        for campo, valor in data.items():
            if hasattr(modelo, campo):
                setattr(modelo, campo, valor)

        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def eliminar(self, id: int):
        modelo = self.session.query(ClienteProcesoHitoCumplimientoModel).filter(
            ClienteProcesoHitoCumplimientoModel.id == id
        ).first()

        if not modelo:
            return False

        self.session.delete(modelo)
        self.session.commit()
        return True
