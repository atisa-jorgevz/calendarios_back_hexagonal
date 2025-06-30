from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.interfaces.schemas.metadato import MetadatoCreate, MetadatoRead, MetadatoUpdate
from app.infrastructure.db.database import SessionLocal
from app.domain.entities.metadato import Metadato
from app.infrastructure.db.repositories.metadato_repositoy_sql import SQLMetadatoRepository
from app.infrastructure.db.repositories.metadatos_area_repository_sql import SQLMetadatosAreaRepository
from app.application.use_cases.metadato.obtener_metadatos_visibles import ObtenerMetadatosVisibles
from app.infrastructure.services.empleado_ceco_provider import EmpleadoCecoProvider

router = APIRouter(prefix="/metadatos", tags=["Metadatos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return SQLMetadatoRepository(db)

@router.get("/", response_model=list[MetadatoRead])
def listar_metadatos(repo = Depends(get_repo)):    
    return repo.get_all()

@router.get("/{metadato_id}", response_model=MetadatoRead)
def obtener_metadato(metadato_id: int, repo = Depends(get_repo)):    
    result = repo.get_by_id(metadato_id)
    if not result:
        raise HTTPException(status_code=404, detail="Metadato no encontrado")
    return result

@router.post("/", response_model=MetadatoRead)
def crear_metadato(payload: MetadatoCreate, repo = Depends(get_repo)):    
    return repo.save(payload)

@router.put("/{metadato_id}", response_model=MetadatoRead)
def actualizar_metadato(
    metadato_id: int,
    payload: MetadatoUpdate,
    repo = Depends(get_repo)
):
    metadato = Metadato(
        id=metadato_id,
        nombre=payload.nombre,
        descripcion=payload.descripcion or "",
        tipo_generacion=payload.tipo_generacion,
        global_=payload.global_,
        activo=payload.activo
    )
    return repo.update(metadato_id, metadato)

@router.delete("/{metadato_id}", status_code=204)
def eliminar_metadato(metadato_id: int, repo = Depends(get_repo)):    
    repo.delete(metadato_id)

@router.get("/visibles/", response_model=list[MetadatoRead])
def obtener_metadatos_visibles(
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    metadato_repo = SQLMetadatoRepository(db)
    area_repo = SQLMetadatosAreaRepository(db)
    ceco_provider = EmpleadoCecoProvider(db)
    use_case = ObtenerMetadatosVisibles(metadato_repo, area_repo, ceco_provider)
    return use_case.execute(email)
