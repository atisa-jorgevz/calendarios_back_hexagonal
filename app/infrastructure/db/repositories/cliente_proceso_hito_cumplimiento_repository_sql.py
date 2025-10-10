# app/infrastructure/db/repositories/cliente_proceso_hito_cumplimiento_repository_sql.py

from app.domain.entities.cliente_proceso_hito_cumplimiento import ClienteProcesoHitoCumplimiento
from app.domain.repositories.cliente_proceso_hito_cumplimiento_repository import ClienteProcesoHitoCumplimientoRepository
from app.infrastructure.db.models.cliente_proceso_hito_cumplimiento_model import ClienteProcesoHitoCumplimientoModel

class ClienteProcesoHitoCumplimientoRepositorySQL(ClienteProcesoHitoCumplimientoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, cliente_proceso_hito_cumplimiento: ClienteProcesoHitoCumplimiento):
        from datetime import datetime

        # Obtener todos los atributos de la entidad
        datos = vars(cliente_proceso_hito_cumplimiento)

        # Filtrar el campo 'id' si es None para evitar problemas con SQLAlchemy
        if datos.get('id') is None:
            datos.pop('id', None)

        # Auto-rellenar fecha_creacion si no está definida
        if datos.get('fecha_creacion') is None:
            datos['fecha_creacion'] = datetime.utcnow()

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

    def obtener_por_cliente_proceso_hito_id(self, cliente_proceso_hito_id: int):
        modelos = self.session.query(ClienteProcesoHitoCumplimientoModel).filter(
            ClienteProcesoHitoCumplimientoModel.cliente_proceso_hito_id == cliente_proceso_hito_id
        ).all()
        return modelos

    def obtener_historial_por_cliente_id(self, cliente_id: str):
        """Obtiene el historial de cumplimientos de un cliente con información completa de proceso e hito"""
        from sqlalchemy import text

        query = text("""
            SELECT cpc.id, cpc.fecha, cpc.hora, cpc.usuario, cpc.observacion, cpc.fecha_creacion,
                   p.id as proceso_id, p.nombre AS proceso, h.id as hito_id, h.nombre AS hito, cph.fecha_limite
            FROM cliente_proceso_hito_cumplimiento cpc
            JOIN cliente_proceso_hito cph ON cph.id = cpc.cliente_proceso_hito_id
            JOIN cliente_proceso cp ON cp.id = cph.cliente_proceso_id
            JOIN proceso p ON p.id = cp.proceso_id
            JOIN hito h ON h.id = cph.hito_id
            WHERE cp.cliente_id = :cliente_id
            ORDER BY cpc.id DESC
        """)

        result = self.session.execute(query, {"cliente_id": cliente_id})
        return result.fetchall()
