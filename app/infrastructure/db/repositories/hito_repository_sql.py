from app.domain.repositories.hito_repository import HitoRepository
from app.domain.entities.hito import Hito
from app.infrastructure.db.models import HitoModel

class HitoRepositorySQL(HitoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, hito: Hito):
        modelo = HitoModel(**vars(hito))
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return modelo

    def listar(self):
        return self.session.query(HitoModel).all()

    def obtener_por_id(self, id: int):
        return self.session.query(HitoModel).filter_by(id=id).first()

    def actualizar(self, id: int, data: dict):
        hito = self.obtener_por_id(id)
        if not hito:
            return None
        for key, value in data.items():
            setattr(hito, key, value)
        self.session.commit()
        self.session.refresh(hito)
        return hito

    def eliminar(self, id: int):
        hito = self.obtener_por_id(id)
        if not hito:
            return None
        self.session.delete(hito)
        self.session.commit()
        return True
