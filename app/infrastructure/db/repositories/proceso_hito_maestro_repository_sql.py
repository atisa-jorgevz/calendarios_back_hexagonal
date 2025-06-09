from app.domain.entities.proceso_hito_maestro import ProcesoHitoMaestro
from app.domain.repositories.proceso_hito_maestro_repository import ProcesoHitoMaestroRepository
from app.infrastructure.db.models import ProcesoHitoMaestroModel

class ProcesoHitoMaestroRepositorySQL(ProcesoHitoMaestroRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, relacion: ProcesoHitoMaestro):
        modelo = ProcesoHitoMaestroModel(**vars(relacion))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def listar(self):
        return self.session.query(ProcesoHitoMaestroModel).all()

    def obtener_por_id(self, id: int):
        return self.session.query(ProcesoHitoMaestroModel).filter_by(id=id).first()
    
    def eliminar(self, id: int):
        relacion = self.obtener_por_id(id)
        if not relacion:
            return None
        self.session.delete(relacion)
        self.session.commit()
        return True

    def listar_por_proceso(self, id_proceso: str):
        return self.session.query(ProcesoHitoMaestroModel).filter_by(id_proceso=id_proceso).all()
