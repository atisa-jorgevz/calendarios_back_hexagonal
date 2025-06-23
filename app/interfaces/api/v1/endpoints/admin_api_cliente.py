import secrets
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.models.api_cliente_model import ApiClienteModel
from app.interfaces.api.api_key_guard import verificar_admin_key
from app.interfaces.api.security.auth import hash_password
from app.interfaces.schemas.cliente_api import CrearClienteAPIRequest, CambiarEstadoClienteRequest,AsociarClientesRequest
from app.application.use_cases.api_clientes.asociar_clientes_api_cliente import AsociarClientesApiCliente
from app.infrastructure.db.repositories.api_cliente_cliente_repository_sql import SqlApiClienteClienteRepository
from app.infrastructure.db.database import get_db


router = APIRouter()

def get_db():    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/api-clientes", tags=["Admin API"], dependencies=[Depends(verificar_admin_key)],
    summary="Listar todos los clientes API",
    description="Devuelve todos los registros de clientes API y sus claves.")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ApiClienteModel).all()



@router.post("/admin/api-clientes", tags=["Admin API"], dependencies=[Depends(verificar_admin_key)],
    summary="Crear nuevo cliente API",
    description="Crea un nuevo cliente API con una clave secreta autogenerada.")
def crear_cliente(
    data: CrearClienteAPIRequest,
    db: Session = Depends(get_db)
):    
    nueva_clave = secrets.token_urlsafe(32)
    hashed_key = hash_password(nueva_clave)

    cliente = ApiClienteModel(
        nombre_cliente=data.nombre_cliente,
        api_key=hashed_key,
        activo=True
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return {
        "mensaje": "Cliente creado",
        "api_key": nueva_clave,
        "cliente": cliente.nombre_cliente
    }

@router.put("/admin/api-clientes/{id}", tags=["Admin API"], dependencies=[Depends(verificar_admin_key)],
    summary="Activar/desactivar cliente API",
    description="Cambia el estado activo de un cliente API existente.")
def cambiar_estado(
    data: CambiarEstadoClienteRequest,
    id: int = Path(..., description="ID del cliente API"),    
    db: Session = Depends(get_db)
    
):
    cliente = db.query(ApiClienteModel).filter_by(id=id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente.activo = data.activo
    db.commit()
    return {
        "mensaje": "Estado actualizado",
        "cliente": cliente.nombre_cliente,
        "activo": cliente.activo
    }

@router.post("/admin/api-clientes/{api_cliente_id}/asociar-clientes")
def asociar_clientes_api_cliente(
    api_cliente_id: int,
    payload: AsociarClientesRequest,
    db=Depends(get_db)
):
    repo = SqlApiClienteClienteRepository(db)
    use_case = AsociarClientesApiCliente(repo)
    use_case.execute(api_cliente_id, payload.cliente_ids)
    return {"message": "Clientes asociados correctamente"}