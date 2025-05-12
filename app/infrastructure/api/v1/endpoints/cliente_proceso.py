from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_proceso_repository_sql import ClienteProcesoRepositorySQL

from app.application.use_cases.cliente_proceso.crear_cliente_proceso import crear_cliente_proceso
from app.application.use_cases.cliente_proceso.listar_cliente_procesos import listar_cliente_procesos
from app.application.use_cases.cliente_proceso.obtener_cliente_proceso import obtener_cliente_proceso
from app.application.use_cases.cliente_proceso.eliminar_cliente_proceso import eliminar_cliente_proceso

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteProcesoRepositorySQL(db)

@router.post("/cliente-procesos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_cliente_proceso(data, repo)

@router.get("/cliente-procesos")
def listar(repo = Depends(get_repo)):
    return listar_cliente_procesos(repo)

@router.get("/cliente-procesos/{id}")
def get(id: int, repo = Depends(get_repo)):
    cliente_proceso = obtener_cliente_proceso(id, repo)
    if not cliente_proceso:
        raise HTTPException(status_code=404, detail="No encontrado")
    return cliente_proceso

@router.get("/cliente-procesos/cliente/{idcliente}")
def get_por_cliente(idcliente: str, repo = Depends(get_repo)):
    return listar_por_cliente(idcliente, repo)

@router.delete("/cliente-procesos/{id}")
def delete(id: int, repo = Depends(get_repo)):
    ok = eliminar_cliente_proceso(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}
