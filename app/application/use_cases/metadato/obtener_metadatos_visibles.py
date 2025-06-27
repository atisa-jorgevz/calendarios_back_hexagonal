from typing import List
from app.domain.entities.metadato import Metadato
from app.domain.repositories.metadato_repository import MetadatoRepository
from app.domain.repositories.metadatos_area_repository import MetadatosAreaRepository
from app.infrastructure.services.empleado_ceco_provider import EmpleadoCecoProvider

class ObtenerMetadatosVisibles:
    def __init__(
        self,
        metadato_repo: MetadatoRepository,
        area_repo: MetadatosAreaRepository,
        ceco_provider: EmpleadoCecoProvider
    ):
        self.metadato_repo = metadato_repo
        self.area_repo = area_repo
        self.ceco_provider = ceco_provider

    def execute(self, email: str) -> List[Metadato]:
        cecos = self.ceco_provider.obtener_cecos_por_email(email)

        globales = [m for m in self.metadato_repo.get_all() if m.global_ == 1]
        areas = self.area_repo.get_by_codigo_ceco_list(cecos)

        # Ahora sí, sacamos los metadatos por área
        metadatos_ceco = [
            self.metadato_repo.get_by_id(area.id_metadato)
            for area in areas
            if area.id_metadato is not None
        ]

        todos = {m.id: m for m in (globales + [m for m in metadatos_ceco if m])}.values()
        return list(todos)
