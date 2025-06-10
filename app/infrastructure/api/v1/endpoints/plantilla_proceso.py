from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.plantilla_proceso_repository_sql import PlantillaProcesoRepositorySQL

from app.application.use_cases.plantilla_proceso.crear_relacion import crear_relacion
from app.application.use_cases.plantilla_proceso.listar_relaciones import listar_relaciones
from app.application.use_cases.plantilla_proceso.listar_procesos_por_plantilla import listar_procesos_por_plantilla
from app.application.use_cases.plantilla_proceso.eliminar_relacion import eliminar_relacion
from app.application.use_cases.plantilla_proceso.eliminar_relacion_por_plantilla import eliminar_relacion_por_plantilla

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return PlantillaProcesoRepositorySQL(db)

@router.post("/plantilla-procesos", tags=["PlantillaProceso"], summary="Crear relación plantilla-proceso",
    description="Crea una relación entre una plantilla y un proceso especificando sus IDs.")
def crear(
    data: dict = Body(..., example={
        "plantilla_id": 1,
        "proceso_id": 2
    }),
    repo = Depends(get_repo)
):
    return crear_relacion(data, repo)

@router.get("/plantilla-procesos", tags=["PlantillaProceso"], summary="Listar relaciones plantilla-proceso",
    description="Devuelve todas las relaciones entre plantillas y procesos.")
def listar(repo = Depends(get_repo)):
    return {
        "plantillaProcesos": listar_relaciones(repo)
    }
@router.get("/plantilla-procesos/plantilla/{id_plantilla}", tags=["PlantillaProceso"], summary="Procesos por plantilla",
    description="Devuelve todos los procesos asociados a una plantilla específica.")
def procesos_por_plantilla(
    id_plantilla: int = Path(..., description="ID de la plantilla a consultar"),
    repo = Depends(get_repo)
):
    return listar_procesos_por_plantilla(id_plantilla, repo)

@router.delete("/plantilla-procesos/{id}", tags=["PlantillaProceso"], summary="Eliminar relación plantilla-proceso",
    description="Elimina una relación específica entre una plantilla y un proceso por su ID.")
def eliminar(
    id: int = Path(..., description="ID de la relación a eliminar"),
    repo = Depends(get_repo)
):
    ok = eliminar_relacion(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"mensaje": "Relación eliminada"}

@router.delete("/plantilla-procesos/plantilla/{id_plantilla}", tags=["PlantillaProceso"], summary="Eliminar todas las relaciones de una plantilla",
    description="Elimina todas las relaciones entre una plantilla y sus procesos asociados.")
def eliminar_por_plantilla(
    id_plantilla: int = Path(..., description="ID de la plantilla cuyas relaciones quieres eliminar"),
    repo = Depends(get_repo)
):
    ok = eliminar_relacion_por_plantilla(id_plantilla, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No se encontraron relaciones para la plantilla")
    return {"mensaje": "Relaciones eliminadas"}
