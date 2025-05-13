import secrets
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.models.api_cliente_model import ApiClienteModel
from app.infrastructure.api.security import verificar_admin_key

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
    data: dict = Body(..., example={"nombre_cliente": "NuevoSistema"}),
    db: Session = Depends(get_db)
):
    nueva_clave = secrets.token_urlsafe(32)
    cliente = ApiClienteModel(nombre_cliente=data["nombre_cliente"], api_key=nueva_clave, activo=True)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return {"mensaje": "Cliente creado", "api_key": cliente.api_key, "cliente": cliente.nombre_cliente}

@router.put("/admin/api-clientes/{id}", tags=["Admin API"], dependencies=[Depends(verificar_admin_key)],
    summary="Activar/desactivar cliente API",
    description="Cambia el estado activo de un cliente API existente.")
def cambiar_estado(
    id: int = Path(..., description="ID del cliente API"),
    data: dict = Body(..., example={"activo": False}),
    db: Session = Depends(get_db)
):
    cliente = db.query(ApiClienteModel).filter_by(id=id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente.activo = data["activo"]
    db.commit()
    return {"mensaje": "Estado actualizado", "cliente": cliente.nombre_cliente, "activo": cliente.activo}
