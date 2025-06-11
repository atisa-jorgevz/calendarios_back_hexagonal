from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.sql_api_cliente_repository import SqlApiClienteRepository
from app.interfaces.api.security.auth import create_access_token, verify_password
from app.config import settings

router = APIRouter()

# Dependency para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token", summary="Login de cliente API y emisión de JWT")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    repo = SqlApiClienteRepository(db)
    cliente = repo.get_by_nombre(form_data.username)

    if not cliente or not cliente.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cliente no encontrado o inactivo")

    if not verify_password(form_data.password, cliente.hashed_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clave incorrecta")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": cliente.nombre_cliente}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
