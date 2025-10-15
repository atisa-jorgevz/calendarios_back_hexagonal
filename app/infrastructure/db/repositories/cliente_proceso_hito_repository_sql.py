# app/infrastructure/db/repositories/cliente_proceso_hito_repository_sql.py

from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito
from app.domain.repositories.cliente_proceso_hito_repository import ClienteProcesoHitoRepository
from app.infrastructure.db.models.cliente_proceso_hito_model import ClienteProcesoHitoModel
from datetime import date, datetime

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

    def listar_habilitados(self):
        """Lista solo los hitos habilitados (habilitado=True)"""
        return self.session.query(ClienteProcesoHitoModel).filter_by(habilitado=True).all()

    def obtener_habilitados_por_cliente_proceso_id(self, cliente_proceso_id: int):
        """Obtiene solo los hitos habilitados de un proceso de cliente específico"""
        return self.session.query(ClienteProcesoHitoModel).filter_by(
            cliente_proceso_id=cliente_proceso_id,
            habilitado=True
        ).all()

    def deshabilitar_desde_fecha_por_hito(self, hito_id: int, fecha_desde):
        """Deshabilita todos los ClienteProcesoHito para un hito_id con fecha_limite >= fecha_desde"""
        # Normalizar fecha_desde a date
        if isinstance(fecha_desde, str):
            try:
                fecha_desde = datetime.fromisoformat(fecha_desde).date()
            except ValueError:
                fecha_desde = date.fromisoformat(fecha_desde)

        query = self.session.query(ClienteProcesoHitoModel).filter(
            ClienteProcesoHitoModel.hito_id == hito_id,
            ClienteProcesoHitoModel.fecha_limite >= fecha_desde
        )
        afectados = 0
        for registro in query.all():
            registro.habilitado = False
            afectados += 1
        self.session.commit()
        return afectados

    def actualizar(self, id: int, data: dict):
        from datetime import datetime, date
        hito = self.obtener_por_id(id)
        if not hito:
            return None

        for key, value in data.items():
            # Manejar conversión de tipos específicos
            if key == 'fecha_estado' and isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    value = datetime.fromisoformat(value)
            elif key == 'fecha_limite' and isinstance(value, str):
                try:
                    value = date.fromisoformat(value)
                except ValueError:
                    value = value
            elif key == 'habilitado' and isinstance(value, str):
                value = value.lower() in ('true', '1', 'yes', 'on')

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
