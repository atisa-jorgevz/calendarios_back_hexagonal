from app.domain.repositories.proceso_repository import ProcesoRepository
from app.domain.entities.proceso import Proceso
from app.infrastructure.db.models import ProcesoModel

class ProcesoRepositorySQL(ProcesoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, proceso: Proceso):
        modelo = ProcesoModel(**vars(proceso))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def actualizar(self, id: int, data: dict):
        proceso = self.session.query(ProcesoModel).filter_by(id=id).first()
        if not proceso:
            return None

        for key, value in data.items():
            setattr(proceso, key, value)

        self.session.commit()
        self.session.refresh(proceso)
        return proceso

    def listar(self):
        return self.session.query(ProcesoModel).all()
    
    def obtener_por_id(self, id: int):
        return self.session.query(ProcesoModel).filter_by(id=id).first()

    def eliminar(self, id: int):
        proceso = self.session.query(ProcesoModel).filter_by(id=id).first()
        if not proceso:
            return None
        self.session.delete(proceso)
        self.session.commit()
        return True