from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.metadatos_area import MetadatosArea
from app.domain.repositories.metadatos_area_repository import MetadatosAreaRepository
from app.infrastructure.db.models.metadatos_area_model import MetadatosAreaModel

class SQLMetadatosAreaRepository(MetadatosAreaRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[MetadatosArea]:
        return [self._to_entity(m) for m in self.session.query(MetadatosAreaModel).all()]

    def get_by_id(self, id: int) -> MetadatosArea | None:
        m = self.session.query(MetadatosAreaModel).filter_by(id=id).first()
        return self._to_entity(m) if m else None

    def save(self, data: MetadatosArea) -> MetadatosArea:
        modelo = MetadatosAreaModel(
            id_metadato=data.id_metadato,
            codigo_ceco=data.codigo_ceco
        )
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return self._to_entity(modelo)

    def delete(self, id: int) -> None:
        self.session.query(MetadatosAreaModel).filter_by(id=id).delete()
        self.session.commit()

    def _to_entity(self, m: MetadatosAreaModel) -> MetadatosArea:
        return MetadatosArea(
            id=m.id,
            id_metadato=m.id_metadato,
            codigo_ceco=m.codigo_ceco
        )
