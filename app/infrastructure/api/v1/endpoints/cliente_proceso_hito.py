# app/infrastructure/api/v1/endpoints/cliente_proceso_hito.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_proceso_hito_repository_sql import ClienteProcesoHitoRepositorySQL

from app.application.use_cases.cliente_proceso_hito.crear_cliente_proceso_hito import crear_cliente_proceso_hito
from app.application.use_cases.cliente_proceso_hito.listar_cliente_proceso_hitos import listar_cliente_proceso_hitos
from app.application.use_cases.cliente_proceso_hito.obtener_cliente_proceso_hitos_por_id import obtener_cliente_proceso_hitos_por_id
from app.application.use_cases.cliente_proceso_hito.eliminar_cliente_proceso_hito import eliminar_cliente_proceso_hito


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteProcesoHitoRepositorySQL(db)

@router.post("/cliente-proceso-hitos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_cliente_proceso_hito(data, repo)

@router.get("/cliente-proceso-hitos")
def listar(repo = Depends(get_repo)):
    return listar_cliente_proceso_hitos(repo)

@router.get("/cliente-proceso-hitos/{id}")
def get(id: int, repo = Depends(get_repo)):
    hito = obtener_cliente_proceso_hitos_por_id(id, repo)
    if not hito:
        raise HTTPException(status_code=404, detail="No encontrado")
    return hito

@router.delete("/cliente-proceso-hitos/{id}")
def delete(id: int, repo = Depends(get_repo)):
    ok = eliminar_cliente_proceso_hito(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}
