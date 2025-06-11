from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.plantilla_repository_sql import PlantillaRepositorySQL

from app.domain.entities.plantilla import Plantilla

from app.application.use_cases.plantillas.update_plantilla import actualizar_plantilla


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return PlantillaRepositorySQL(db)

# Crear un nuevo plantilla
@router.post("/plantillas")
def crear(data: dict = Body(..., example={"nombre": "Plantilla Fiscal", "descripcion": "Para procesos fiscales"}), repo = Depends(get_repo)):
    plantilla = Plantilla(
        nombre=data.get("nombre"),
        descripcion=data.get("descripcion"),
    )
    return repo.crear(plantilla)

# Listar todos los plantillas
@router.get("/plantillas")
def listar(
    page: Optional[int] = Query(None, ge=1, description="Página actual"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Cantidad de resultados por página"),
    repo = Depends(get_repo)
):
    plantillas = repo.listar()
    total = len(plantillas)

    if page is not None and limit is not None:
        start = (page - 1) * limit
        end = start + limit
        plantillas = plantillas[start:end]

    if not plantillas:
        raise HTTPException(status_code=404, detail="No se encontraron plantillas")

    return {
        "total": total,
        "plantillas": plantillas
    }

# Obtener un plantilla por ID
@router.get("/plantillas/{id}", tags=["Plantillas"])
def get_plantilla(id: int, repo = Depends(get_repo)):
    """
    Devuelve una plantilla con campos:
    - id
    - nombre
    - descripcion
    """
    plantilla = repo.obtener_por_id(id)
    if not plantilla:
        raise HTTPException(status_code=404, detail="plantilla no encontrado")
    return plantilla

# Actualizar un plantilla
@router.put("/plantillas/{id}")
def update(id: int, data: dict, repo = Depends(get_repo)):
    actualizado = actualizar_plantilla(id, data, repo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="plantilla no encontrado")
    return actualizado

# Eliminar un plantilla
@router.delete("/plantillas/{id}")
def delete_plantilla(id: int, repo = Depends(get_repo)):
    resultado = repo.eliminar(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="plantilla no encontrado")
    return {"mensaje": "plantilla eliminado"}
