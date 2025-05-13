from fastapi import APIRouter, Depends, HTTPException, Path
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

@router.get("/clientes", tags=["Clientes"], summary="Listar clientes",
    description="Devuelve la lista completa de clientes registrados en el sistema.")
def obtener_todos(repo = Depends(get_repo)):
    clientes = listar_clientes(repo)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes")
    return clientes

@router.get("/clientes/nombre/{nombre}", tags=["Clientes"], summary="Buscar clientes por nombre",
    description="Busca clientes que contengan el nombre proporcionado.")
def buscar_nombre(
    nombre: str = Path(..., description="Nombre (o parte) del cliente a buscar"),
    repo = Depends(get_repo)
):
    clientes = buscar_cliente_por_nombre(nombre, repo)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes con ese nombre")
    return clientes

@router.get("/clientes/cif/{cif}", tags=["Clientes"], summary="Buscar cliente por CIF",
    description="Busca un cliente específico por su CIF.")
def buscar_cif(
    cif: str = Path(..., description="CIF del cliente a buscar"),
    repo = Depends(get_repo)
):
    cliente = buscar_cliente_por_cif(cif, repo)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
