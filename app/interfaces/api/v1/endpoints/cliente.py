from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_repository_sql import ClienteRepositorySQL

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
def obtener_todos(
    page: Optional[int] = Query(None, ge=1, description="Página actual"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Cantidad de resultados por página"),
    repo = Depends(get_repo)
):
    clientes = repo.listar()
    total = len(clientes)

    if page is not None and limit is not None:
        start = (page - 1) * limit
        end = start + limit
        clientes = clientes[start:end]

    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes")

    return {
        "total": total,
        "clientes": clientes
    }

@router.get("/clientes/nombre/{nombre}", tags=["Clientes"], summary="Buscar clientes por nombre",
    description="Busca clientes que contengan el nombre proporcionado.")
def buscar_nombre(
    nombre: str = Path(..., description="Nombre (o parte) del cliente a buscar"),
    repo = Depends(get_repo)
):
    clientes = repo.buscar_por_nombre(nombre)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes con ese nombre")
    return clientes

@router.get("/clientes/cif/{cif}", tags=["Clientes"], summary="Buscar cliente por CIF",
    description="Busca un cliente específico por su CIF.")
def buscar_cif(
    cif: str = Path(..., description="CIF del cliente a buscar"),
    repo = Depends(get_repo)
):
    cliente = repo.buscar_por_cif(cif)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
