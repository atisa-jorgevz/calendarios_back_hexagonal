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
