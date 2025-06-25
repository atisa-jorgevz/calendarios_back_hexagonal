from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.domain.repositories.documento_repository import DocumentoRepository
from app.interfaces.schemas.documento import DocumentoCreate, DocumentoRead
from app.infrastructure.db.repositories.documento_repository_sql import SQLDocumentoRepository
from app.infrastructure.db.repositories.cliente_proceso_hito_repository_sql import ClienteProcesoHitoRepositorySQL
from app.application.use_cases.documento.crear_documento import CrearDocumentoUseCase


router = APIRouter(prefix="/documentos", tags=["Documentos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return SQLDocumentoRepository(db)

def get_repo_cliente_proceso_hito(db: Session = Depends(get_db)):
    return ClienteProcesoHitoRepositorySQL(db)

@router.get("/", response_model=list[DocumentoRead])
def listar(repo: DocumentoRepository = Depends(get_repo)):
    return repo.get_all()

@router.get("/{id}", response_model=DocumentoRead)
def obtener(id: int, repo: DocumentoRepository = Depends(get_repo)):
    doc = repo.get_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@router.post("/", response_model=DocumentoRead)
def crear(payload: DocumentoCreate, repo: DocumentoRepository = Depends(get_repo), repo_cliente_proceso_hito: ClienteProcesoHitoRepositorySQL = Depends(get_repo_cliente_proceso_hito)):

    use_case = CrearDocumentoUseCase(repo, repo_cliente_proceso_hito)
    try:
        return use_case.execute(
            id_cliente_proceso_hito=payload.id_cliente_proceso_hito,
            nombre_documento=payload.nombre_documento
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", status_code=204)
def eliminar(id: int, repo: DocumentoRepository = Depends(get_repo)):
    repo.delete(id)
