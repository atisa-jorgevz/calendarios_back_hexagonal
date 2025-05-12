from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_repository_sql import ClienteRepositorySQL

from app.application.use_cases.clientes.listar_clientes import listar_clientes
from app.application.use_cases.clientes.buscar_cliente_por_nombre import buscar_cliente_por_nombre
from app.application.use_cases.clientes.buscar_cliente_por_cif import buscar_cliente_por_cif

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteRepositorySQL(db)

@router.get("/clientes")
def obtener_todos(repo = Depends(get_repo)):
    clientes = listar_clientes(repo)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes")
    return clientes

@router.get("/clientes/nombre/{nombre}")
def buscar_nombre(nombre: str, repo = Depends(get_repo)):
    clientes = buscar_cliente_por_nombre(nombre, repo)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes con ese nombre")
    return clientes

@router.get("/clientes/cif/{cif}")
def buscar_cif(cif: str, repo = Depends(get_repo)):
    cliente = buscar_cliente_por_cif(cif, repo)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
