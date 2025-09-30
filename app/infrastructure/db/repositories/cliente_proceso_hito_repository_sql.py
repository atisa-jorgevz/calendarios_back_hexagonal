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

    def actualizar(self, id: int, data: dict):
        hito = self.obtener_por_id(id)
        if not hito:
            return None
        for key, value in data.items():
            setattr(hito, key, value)
        self.session.commit()
        self.session.refresh(hito)
        return hito

    def verificar_registros_por_hito(self, hito_id: int):
        """Verifica si existe algún registro para un hito específico"""
        from app.infrastructure.db.models import ProcesoHitoMaestroModel

        # Buscar cualquier registro en cliente_proceso_hito que referencie al hito a través de proceso_hito_maestro
        resultado = self.session.query(ClienteProcesoHitoModel).join(
            ProcesoHitoMaestroModel,
            ClienteProcesoHitoModel.hito_id == ProcesoHitoMaestroModel.hito_id
        ).filter(
            ProcesoHitoMaestroModel.hito_id == hito_id
        ).first()

        return resultado is not None

    def eliminar_por_hito_id(self, hito_id: int):
        """Elimina todos los registros de cliente_proceso_hito asociados a un hito específico"""
        from app.infrastructure.db.models import ProcesoHitoMaestroModel

        # Obtener los IDs de proceso_hito_maestro que referencian al hito
        proceso_hito_ids = self.session.query(ProcesoHitoMaestroModel.id).filter(
            ProcesoHitoMaestroModel.hito_id == hito_id
        ).all()

        if proceso_hito_ids:
            # Extraer solo los IDs
            ids_list = [phm_id[0] for phm_id in proceso_hito_ids]

            # Eliminar registros de cliente_proceso_hito que referencien estos IDs
            eliminados = self.session.query(ClienteProcesoHitoModel).filter(
                ClienteProcesoHitoModel.hito_id.in_(ids_list)
            ).delete(synchronize_session=False)

            self.session.commit()
            return eliminados

        return 0
