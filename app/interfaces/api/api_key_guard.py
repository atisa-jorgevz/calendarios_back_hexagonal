import os
from fastapi import Header, HTTPException, Depends, Request
from typing import Optional
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_db
from app.infrastructure.services.cliente_api_service_impl import ClienteAPIServiceImpl
from app.config import settings

def verificar_api_key(request: Request, db: Session = Depends(get_db)):
    if request.method == "OPTIONS":        
        return

    x_api_key = request.headers.get("x_api_key")
    
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Falta la API Key")

    auth_service = ClienteAPIServiceImpl(db)
    if not auth_service.validar_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="API Key inválida o no autorizada")

def verificar_admin_key(x_admin_api_key: str = Header(..., description="Clave de administración interna")):
    
    if x_admin_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="No autorizado como administrador")
