import app.domain.repositories.plantilla_proceso_repository as PlantillaProcesoRepository

def listar_procesos_por_plantilla(id_plantilla: int, repo: PlantillaProcesoRepository):    
    return repo.listar_procesos_por_plantilla(id_plantilla)