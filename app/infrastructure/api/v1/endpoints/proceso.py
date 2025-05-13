from typing import Optional
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.proceso_repository_sql import ProcesoRepositorySQL

from app.application.use_cases.procesos.crear_proceso import crear_proceso
from app.application.use_cases.procesos.listar_procesos import listar_procesos
from app.application.use_cases.procesos.update_proceso import actualizar_proceso
from app.application.use_cases.procesos.get_proceso import obtener_proceso
from app.application.use_cases.procesos.delete_proceso import eliminar_proceso
from app.application.use_cases.procesos.listar_procesos_cliente_por_empleado import listar_procesos_cliente_por_empleado

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ProcesoRepositorySQL(db)

# Crear un nuevo proceso
@router.post("/procesos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_proceso(data, repo)

@router.get("/procesos/procesos-cliente-por-empleado")
def procesos_cliente_por_empleado(
    email: str = Query(..., description="Email del empleado que hace la consulta"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha mínima (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha máxima (YYYY-MM-DD)"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mes de inicio (1-12)"),
    anio: Optional[int] = Query(None, ge=2000, le=2100, description="Año de inicio (ej: 2024)"),
    repo = Depends(get_repo)
):
    """
    Devuelve en UNA sola llamada a BD todos los procesos (con sus hitos)
    de los clientes asociados al email de empleado que le pases como query param.
    Ejemplo: GET /procesos/mis-clientes-optimo?email=mi@empleado.com
    """
    return listar_procesos_cliente_por_empleado(
        email=email,
        repo=repo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        mes=mes,
        anio=anio
    )

# Listar todos los procesos
@router.get("/procesos")
def listar(repo = Depends(get_repo)):
    procesos = listar_procesos(repo)
    if not procesos:
        raise HTTPException(status_code=404, detail="No se encontraron procesos")
    return procesos

# Obtener un proceso por ID
@router.get("/procesos/{id}")
def get_proceso(id: int, repo = Depends(get_repo)):
    proceso = obtener_proceso(id, repo)
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return proceso

# Actualizar un proceso
@router.put("/procesos/{id}")
def update(id: int, data: dict, repo = Depends(get_repo)):
    actualizado = actualizar_proceso(id, data, repo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return actualizado

# Eliminar un proceso
@router.delete("/procesos/{id}")
def delete_proceso(id: int, repo = Depends(get_repo)):
    resultado = eliminar_proceso(id, repo)
    if not resultado:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return {"mensaje": "Proceso eliminado"}

