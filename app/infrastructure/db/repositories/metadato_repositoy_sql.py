from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.metadato import Metadato
from app.domain.repositories.metadato_repository import MetadatoRepository
from app.infrastructure.db.models.metadato_model import MetadatoModel

class SQLMetadatoRepository(MetadatoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Metadato]:
        registros = self.session.query(MetadatoModel).all()
        return [self._to_entity(m) for m in registros]

    def get_by_id(self, metadato_id: int) -> Metadato | None:
        modelo = self.session.query(MetadatoModel).filter_by(id=metadato_id).first()
        return self._to_entity(modelo) if modelo else None

    def save(self, metadato: Metadato) -> Metadato:        
        modelo = MetadatoModel(
            nombre=metadato.nombre,
            descripcion=metadato.descripcion,
            tipo_generacion=metadato.tipo_generacion,
            global_=metadato.global_,
            activo=metadato.activo
        )
        self.session.add(modelo)

        self.session.commit()
        return self._to_entity(modelo)

    def update(self, metadato_id: int, metadato: Metadato) -> Metadato:
        modelo = self.session.query(MetadatoModel).get(metadato_id)
        if not modelo:
            raise Exception("Metadato no encontrado")

        modelo.nombre = metadato.nombre
        modelo.descripcion = metadato.descripcion
        modelo.tipo_generacion = metadato.tipo_generacion
        modelo.global_ = metadato.global_
        modelo.activo = metadato.activo

        self.session.commit()
        return self._to_entity(modelo)


    def delete(self, metadato_id: int) -> None:
        self.session.query(MetadatoModel).filter_by(id=metadato_id).delete()
        self.session.commit()

    def _to_entity(self, modelo: MetadatoModel) -> Metadato:
        return Metadato(
            id=modelo.id,
            nombre=modelo.nombre,
            descripcion=modelo.descripcion,
            tipo_generacion=modelo.tipo_generacion,
            global_=modelo.global_,
            activo=modelo.activo
        )
