from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.entities.cliente import Cliente
from app.infrastructure.db.models.cliente_model import ClienteModel

class ClienteRepositorySQL(ClienteRepository):
    def __init__(self, session: Session):
        self.session = session

    def listar(self) -> List[Cliente]:
        registros = self.session.query(ClienteModel).all()
        return [self._mapear_modelo_a_entidad(r) for r in registros]

    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        registros = self.session.query(ClienteModel).filter(
            ClienteModel.razsoc.ilike(f"%{nombre}%")
        ).all()
        return [self._mapear_modelo_a_entidad(r) for r in registros]

    def buscar_por_cif(self, cif: str) -> Optional[Cliente]:
        registro = self.session.query(ClienteModel).filter_by(cif=cif).first()
        return self._mapear_modelo_a_entidad(registro) if registro else None
# si alguno de los que lean este codigo se pregunta porque demonios hemos hecho esta funcion...le doy 2 tiros...no es coña,
# la razon es porque esta entidad no depende de este backend, sino que es una entidad externa, que puede ser que cambie, es deicr que se le pongan campos por ejemplo o camvias nombres....
# con esto evitamos que si esto sucede pues no reviente nuestro back.
    def _mapear_modelo_a_entidad(self, modelo: ClienteModel) -> Cliente:
        return Cliente(
            idcliente=modelo.idcliente,
            cif=modelo.cif,
            cif_empresa=modelo.cif_empresa,
            razsoc=modelo.razsoc,
            direccion=modelo.direccion,
            localidad=modelo.localidad,
            provincia=modelo.provincia,
            cpostal=modelo.cpostal,
            codigop=modelo.codigop,
            pais=modelo.pais,
            cif_factura=modelo.cif_factura,
        )

    def obtener_por_id(self, id: str) -> Optional[Cliente]:
        registro = self.session.query(ClienteModel).filter_by(idcliente=id).first()
        return self._mapear_modelo_a_entidad(registro) if registro else None
