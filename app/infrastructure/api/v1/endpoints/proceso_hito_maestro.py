from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.proceso_hito_maestro_repository_sql import ProcesoHitoMaestroRepositorySQL
from app.application.use_cases.proceso_hito_maestro.crear_relacion import crear_relacion
from app.application.use_cases.proceso_hito_maestro.listar_relaciones import listar_relaciones

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ProcesoHitoMaestroRepositorySQL(db)

@router.post("/proceso-hitos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_relacion(data, repo)

@router.get("/proceso-hitos")
def listar(repo = Depends(get_repo)):
    return listar_relaciones(repo)
