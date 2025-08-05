from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_proceso_hito_repository_sql import ClienteProcesoHitoRepositorySQL

from app.domain.entities.cliente_proceso_hito import ClienteProcesoHito

router = APIRouter(prefix="/cliente-proceso-hitos", tags=["ClienteProcesoHito"])

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
        "fecha_estado": "2023-01-01",
        "hora_limite": "12:00:00",
        "tipo": "Atisa"
    }),
    repo = Depends(get_repo)
):
    hito = ClienteProcesoHito(
        cliente_proceso_id=data["cliente_proceso_id"],
        hito_id=data["hito_id"],
        estado=data["estado"],
        fecha_estado=data.get("fecha_estado"),
        fecha_inicio=data["fecha_inicio"],
        fecha_fin=data.get("fecha_fin"),
        hora_limite=data.get("hora_limite"),
        tipo=data["tipo"]
    )
    return repo.guardar(hito)

@router.get("/", summary="Listar todas las relaciones cliente-proceso-hito",
    description="Devuelve todas las relaciones entre clientes, procesos e hitos registradas.")
def listar(repo = Depends(get_repo)):
    return repo.listar()

@router.get("/{id}", summary="Obtener relación por ID",
    description="Devuelve una relación cliente-proceso-hito específica según su ID.")
def get(
    id: int = Path(..., description="ID de la relación a consultar"),
    repo = Depends(get_repo)
):
    hito = repo.obtener_por_id(id)
    if not hito:
        raise HTTPException(status_code=404, detail="No encontrado")
    return hito

@router.put("/{id}", summary="Actualizar relación cliente-proceso-hito",
    description="Actualiza una relación cliente-proceso-hito existente por su ID.")
def actualizar(
    id: int = Path(..., description="ID de la relación a actualizar"),
    data: dict = Body(..., example={
        "estado": "completado",
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2023-01-05",
        "fecha_estado": "2023-01-05"
    }),
    repo = Depends(get_repo)
):
    hito_actualizado = repo.actualizar(id, data)
    if not hito_actualizado:
        raise HTTPException(status_code=404, detail="No encontrado")
    return hito_actualizado

@router.delete("/{id}", summary="Eliminar relación",
    description="Elimina una relación cliente-proceso-hito existente por su ID.")
def delete(
    id: int = Path(..., description="ID de la relación a eliminar"),
    repo = Depends(get_repo)
):
    ok = repo.eliminar(id)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}

@router.get("/cliente-proceso/{id_cliente_proceso}", summary="Listar hitos de un proceso de cliente",
    description="Devuelve todos los hitos asociados a un proceso de cliente específico.")
def get_hitos_por_proceso(
    id_cliente_proceso: int = Path(..., description="ID del proceso de cliente"),
    repo = Depends(get_repo)
):
    hitos = repo.obtener_por_cliente_proceso_id(id_cliente_proceso)
    if not hitos:
        raise HTTPException(status_code=404, detail="No se encontraron hitos para este proceso")
    return hitos
