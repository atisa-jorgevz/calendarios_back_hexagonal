from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.proceso_hito_maestro_repository_sql import ProcesoHitoMaestroRepositorySQL
from app.application.use_cases.proceso_hito_maestro.crear_relacion import crear_relacion


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ProcesoHitoMaestroRepositorySQL(db)

@router.post("/proceso-hitos", tags=["ProcesoHitoMaestro"], summary="Crear relación proceso-hito",
    description="Crea una relación entre un proceso y un hito, especificando sus IDs.")
def crear(
    data: dict = Body(..., example={
        "id_proceso": 1,
        "id_hito": 2
    }),
    repo = Depends(get_repo)
):
    return crear_relacion(data, repo)

@router.get("/proceso-hitos", tags=["ProcesoHitoMaestro"], summary="Listar relaciones proceso-hito",
    description="Devuelve todas las relaciones entre procesos e hitos registradas.")
def listar(repo = Depends(get_repo)):
    return {
        "procesoHitos" : repo.listar()
    }


@router.delete("/proceso-hitos/{id}", tags=["ProcesoHitoMaestro"], summary="Eliminar relación proceso-hito",
    description="Elimina una relación entre un proceso y un hito por su ID.")
def delete(
    id: int = Path(..., description="ID de la relación a eliminar"),
    repo = Depends(get_repo)
):
    resultado = repo.eliminar(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="relacion no encontrada")
    return {"mensaje": "relacion eliminada"}
