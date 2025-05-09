# app/infrastructure/api/v1/endpoints/plantilla_proceso.py

from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/plantilla-procesos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_relacion(data, repo)

@router.get("/plantilla-procesos")
def listar(repo = Depends(get_repo)):
    return listar_relaciones(repo)

@router.get("/plantilla-procesos/plantilla/{id_plantilla}")
def procesos_por_plantilla(id_plantilla: int, repo = Depends(get_repo)):
    return listar_procesos_por_plantilla(id_plantilla, repo)

@router.delete("/plantilla-procesos/{id}")
def eliminar(id: int, repo = Depends(get_repo)):
    ok = eliminar_relacion(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"mensaje": "Relación eliminada"}

@router.delete("/plantilla-procesos/plantilla/{id_plantilla}")
def eliminar_por_plantilla(id_plantilla: int, repo = Depends(get_repo)):
    ok = eliminar_relacion_por_plantilla(id_plantilla, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No se encontraron relaciones para la plantilla")
    return {"mensaje": "Relaciones eliminadas"}
