import os
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_db
from app.infrastructure.services.cliente_api_service_impl import ClienteAPIServiceImpl

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "clave_admin_ultra_secreta")

def verificar_api_key(
    x_api_key: str = Header(..., description="Clave de API proporcionada por el cliente"),
    db: Session = Depends(get_db)
):
    auth_service = ClienteAPIServiceImpl(db)
    if not auth_service.validar_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="API Key inválida o no autorizada")

def verificar_admin_key(x_admin_key: str = Header(..., description="Clave de administración interna")):
    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="No autorizado como administrador")
