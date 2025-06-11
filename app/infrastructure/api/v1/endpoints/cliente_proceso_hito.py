from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_proceso_hito_repository_sql import ClienteProcesoHitoRepositorySQL

from app.application.use_cases.cliente_proceso_hito.crear_cliente_proceso_hito import crear_cliente_proceso_hito
from app.application.use_cases.cliente_proceso_hito.listar_cliente_proceso_hitos import listar_cliente_proceso_hitos
from app.application.use_cases.cliente_proceso_hito.obtener_cliente_proceso_hitos_por_id import obtener_cliente_proceso_hitos_por_id
from app.application.use_cases.cliente_proceso_hito.eliminar_cliente_proceso_hito import eliminar_cliente_proceso_hito
from app.application.use_cases.cliente_proceso_hito.obtener_cliente_proceso_hitos_por_cliente_proceso_id import obtener_cliente_proceso_hitos_por_cliente_proceso_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteProcesoHitoRepositorySQL(db)

@router.post("/cliente-proceso-hitos", tags=["ClienteProcesoHito"], summary="Crear relación cliente-proceso-hito",
    description="Crea una nueva relación entre un cliente, proceso e hito especificando los IDs correspondientes y fechas.")
def crear(
    data: dict = Body(..., example={
        "cliente_proceso_id": 1,
        "hito_id": 2,
        "estado": "pendiente",
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2023-01-05",
        "fecha_estado": "2023-01-01"
    }),
    repo = Depends(get_repo)
):
    return crear_cliente_proceso_hito(data, repo)

@router.get("/cliente-proceso-hitos", tags=["ClienteProcesoHito"], summary="Listar todas las relaciones cliente-proceso-hito",
    description="Devuelve todas las relaciones entre clientes, procesos e hitos registradas.")
def listar(repo = Depends(get_repo)):
    return listar_cliente_proceso_hitos(repo)

@router.get("/cliente-proceso-hitos/{id}", tags=["ClienteProcesoHito"], summary="Obtener relación por ID",
    description="Devuelve una relación cliente-proceso-hito específica según su ID.")
def get(
    id: int = Path(..., description="ID de la relación a consultar"),
    repo = Depends(get_repo)
):
    hito = obtener_cliente_proceso_hitos_por_id(id, repo)
    if not hito:
        raise HTTPException(status_code=404, detail="No encontrado")
    return hito

@router.delete("/cliente-proceso-hitos/{id}", tags=["ClienteProcesoHito"], summary="Eliminar relación",
    description="Elimina una relación cliente-proceso-hito existente por su ID.")
def delete(
    id: int = Path(..., description="ID de la relación a eliminar"),
    repo = Depends(get_repo)
):
    ok = eliminar_cliente_proceso_hito(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}

@router.get("/cliente-proceso-hitos/cliente-proceso/{id_cliente_proceso}", tags=["ClienteProcesoHito"], summary="Listar hitos de un proceso de cliente",
    description="Devuelve todos los hitos asociados a un proceso de cliente específico.")
def get_hitos_por_proceso(
    id_cliente_proceso: int = Path(..., description="ID del proceso de cliente"),
    repo = Depends(get_repo)
):
    hitos = obtener_cliente_proceso_hitos_por_cliente_proceso_id(id_cliente_proceso, repo)
    if not hitos:
        raise HTTPException(status_code=404, detail="No se encontraron hitos para este proceso")
    return hitos
