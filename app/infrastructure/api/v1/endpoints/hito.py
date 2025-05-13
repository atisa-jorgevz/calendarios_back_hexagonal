from typing import Optional
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.hito_repository_sql import HitoRepositorySQL

from app.application.use_cases.hitos.crear_hito import crear_hito
from app.application.use_cases.hitos.listar_hitos import listar_hitos
from app.application.use_cases.hitos.update_hito import actualizar_hito
from app.application.use_cases.hitos.get_hito import obtener_hito
from app.application.use_cases.hitos.delete_hito import eliminar_hito
from app.application.use_cases.hitos.listar_hitos_cliente_por_empleado import listar_hitos_cliente_por_empleado

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return HitoRepositorySQL(db)

# Crear un nuevo hito
@router.post("/hitos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_hito(data, repo)


@router.get("/hitos/hitos-cliente-por-empleado")
def obtener_hitos_por_empleado(
    email: str = Query(..., description="Email del empleado para obtener los clientes asociados"),
    repo=  Depends(get_repo),
    fecha_inicio: Optional[str] = Query(None, description="Fecha mínima (YYYY-MM-DD) de inicio del hito"),
    fecha_fin: Optional[str] = Query(None, description="Fecha máxima (YYYY-MM-DD) de inicio del hito"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mes de inicio del hito (1-12)"),
    anio: Optional[int] = Query(None, ge=2000, le=2100, description="Año de inicio del hito (ej. 2024)")    
):
    return listar_hitos_cliente_por_empleado(email,repo,fecha_inicio,fecha_fin,mes,anio)

# Listar todos los hitos
@router.get("/hitos")
def listar(repo = Depends(get_repo)):
    hitos = listar_hitos(repo)
    if not hitos:
        raise HTTPException(status_code=404, detail="No se encontraron hitos")
    return hitos

# Obtener un hito por ID
@router.get("/hitos/{id}")
def get_hito(id: int, repo = Depends(get_repo)):
    hito = obtener_hito(id, repo)
    if not hito:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return hito

# Actualizar un hito
@router.put("/hitos/{id}")
def update(id: int, data: dict, repo = Depends(get_repo)):
    actualizado = actualizar_hito(id, data, repo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return actualizado

# Eliminar un hito
@router.delete("/hitos/{id}")
def delete_hito(id: int, repo = Depends(get_repo)):
    resultado = eliminar_hito(id, repo)
    if not resultado:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return {"mensaje": "Hito eliminado"}

