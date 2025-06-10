from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
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

@router.post("/hitos", tags=["Hitos"], summary="Crear un nuevo hito",
    description="Crea un nuevo hito especificando nombre, fechas y si es obligatorio.")
def crear(
    data: dict = Body(..., example={
        "nombre": "Recibir documentos",
        "frecuencia": 1,
        "temporalidad": "mes",
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2023-01-05",
        "obligatorio": 1
    }),
    repo = Depends(get_repo)
):
    return crear_hito(data, repo)

@router.get("/hitos/hitos-cliente-por-empleado", tags=["Hitos"], summary="Listar hitos por cliente/empleado",
    description="Devuelve todos los hitos asociados a los procesos de clientes gestionados por un empleado. Filtrable por fecha de inicio, fin, mes y año.")
def obtener_hitos_por_empleado(
    email: str = Query(..., description="Email del empleado"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha mínima (YYYY-MM-DD) de inicio del hito"),
    fecha_fin: Optional[str] = Query(None, description="Fecha máxima (YYYY-MM-DD) de inicio del hito"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mes de inicio del hito (1-12)"),
    anio: Optional[int] = Query(None, ge=2000, le=2100, description="Año de inicio del hito"),
    repo = Depends(get_repo)
):
    return listar_hitos_cliente_por_empleado(email, repo, fecha_inicio, fecha_fin, mes, anio)

@router.get("/hitos", tags=["Hitos"], summary="Listar todos los hitos",
    description="Devuelve todos los hitos definidos en el sistema.")
def listar(
    page: Optional[int] = Query(None, ge=1, description="Página actual"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Cantidad de resultados por página"),
    repo = Depends(get_repo)
):
    hitos = listar_hitos(repo)
    total = len(hitos)

    if page is not None and limit is not None:
        start = (page - 1) * limit
        end = start + limit
        hitos = hitos[start:end]

    if not hitos:
        raise HTTPException(status_code=404, detail="No se encontraron hitos")

    return {
        "total": total,
        "hitos": hitos
    }

@router.get("/hitos/{id}", tags=["Hitos"], summary="Obtener hito por ID",
    description="Devuelve la información de un hito específico por su ID.")
def get_hito(
    id: int = Path(..., description="ID del hito a consultar"),
    repo = Depends(get_repo)
):
    hito = obtener_hito(id, repo)
    if not hito:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return hito

@router.put("/hitos/{id}", tags=["Hitos"], summary="Actualizar hito",
    description="Actualiza un hito existente por su ID.")
def update(
    id: int = Path(..., description="ID del hito a actualizar"),
    data: dict = Body(..., example={
        "nombre": "Recibir y validar documentos",
        "frecuencia": 1,
        "temporalidad": "mes",
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2023-01-10",
        "obligatorio": 1
    }),
    repo = Depends(get_repo)
):
    actualizado = actualizar_hito(id, data, repo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return actualizado

@router.delete("/hitos/{id}", tags=["Hitos"], summary="Eliminar hito",
    description="Elimina un hito por su ID.")
def delete_hito(
    id: int = Path(..., description="ID del hito a eliminar"),
    repo = Depends(get_repo)
):
    resultado = eliminar_hito(id, repo)
    if not resultado:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    return {"mensaje": "Hito eliminado"}
