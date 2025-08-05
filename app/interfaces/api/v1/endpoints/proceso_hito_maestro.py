from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.proceso_hito_maestro_repository_sql import ProcesoHitoMaestroRepositorySQL
from app.domain.entities.proceso_hito_maestro import ProcesoHitoMaestro


router = APIRouter(prefix="/proceso-hitos", tags=["ProcesoHitoMaestro"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ProcesoHitoMaestroRepositorySQL(db)

@router.post("/", summary="Crear relación proceso-hito",
    description="Crea una relación entre un proceso y un hito, especificando sus IDs.")
def crear(
    data: dict = Body(..., example={
        "id_proceso": 1,
        "id_hito": 2
    }),
    repo = Depends(get_repo)
):
    relacion = ProcesoHitoMaestro(
        id_proceso=data["id_proceso"],
        id_hito=data["id_hito"]
    )
    return repo.guardar(relacion)

@router.get("/", summary="Listar relaciones proceso-hito",
    description="Devuelve todas las relaciones entre procesos e hitos registradas.")
def listar(repo = Depends(get_repo)):
    return {
        "procesoHitos" : repo.listar()
    }


@router.delete("/{id}", summary="Eliminar relación proceso-hito",
    description="Elimina una relación entre un proceso y un hito por su ID.")
def delete(
    id: int = Path(..., description="ID de la relación a eliminar"),
    repo = Depends(get_repo)
):
    resultado = repo.eliminar(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="relacion no encontrada")
    return {"mensaje": "relacion eliminada"}
