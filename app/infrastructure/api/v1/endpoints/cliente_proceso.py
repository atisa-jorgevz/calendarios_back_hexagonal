from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.interfaces.schemas.cliente_proceso import GenerarClienteProcesoRequest
from app.infrastructure.db.repositories.cliente_proceso_repository_sql import ClienteProcesoRepositorySQL
from app.infrastructure.db.repositories.proceso_repository_sql import ProcesoRepositorySQL

from app.application.use_cases.cliente_proceso.crear_cliente_proceso import crear_cliente_proceso
from app.application.use_cases.cliente_proceso.listar_cliente_procesos import listar_cliente_procesos
from app.application.use_cases.cliente_proceso.obtener_cliente_proceso import obtener_cliente_proceso
from app.application.use_cases.cliente_proceso.eliminar_cliente_proceso import eliminar_cliente_proceso
from app.application.use_cases.cliente_proceso.listar_por_cliente import listar_por_cliente
from app.application.use_cases.cliente_proceso.generar_calendario_cliente_proceso import generar_calendario_cliente_proceso

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteProcesoRepositorySQL(db)

def get_repo_proceso(db: Session = Depends(get_db)):    
    return ProcesoRepositorySQL(db)

@router.post("/cliente-procesos")
def crear(data: dict, repo = Depends(get_repo)):
    return crear_cliente_proceso(data, repo)

@router.post("/generar-calendario-cliente-proceso")
def generar_calendario_cliente_by_proceso(request: GenerarClienteProcesoRequest, repo = Depends(get_repo), proceso_repo = Depends(get_repo_proceso)):
    proceso_maestro = proceso_repo.obtener_por_id(request.id_proceso) #esto podria hacerse tambien en vez de mediante el repo, con el caso de uso...
    return generar_calendario_cliente_proceso(request,proceso_maestro, repo)



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
def get_por_cliente(idcliente: int, repo = Depends(get_repo)):
    return listar_por_cliente(idcliente, repo)

@router.delete("/cliente-procesos/{id}")
def delete(id: int, repo = Depends(get_repo)):
    ok = eliminar_cliente_proceso(id, repo)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}
