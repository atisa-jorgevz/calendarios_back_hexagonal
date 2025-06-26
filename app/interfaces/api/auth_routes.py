from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.sql_api_cliente_repository import SqlApiClienteRepository
from app.interfaces.api.security.auth import create_access_token, verify_password,create_refresh_token
from app.config import settings
from app.interfaces.schemas.token import RefreshTokenRequest, TokenResponse
from app.infrastructure.services.sso_service import SSOService
from app.infrastructure.services.user_mapping_service_impl import UserMappingServiceImpl


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
    access_token = create_access_token(
        data={
            "sub": cliente.nombre_cliente,
            "id_api_cliente": cliente.id,
            "atisa": False
        },
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": cliente.nombre_cliente})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token_view(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

        return {"access_token": new_access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido o caducado")


@router.get("/sso/login", summary="Inicia el proceso de Single Sign-On")
def sso_login():
    """
    Inicia el proceso de autenticación SSO con Microsoft Azure AD.
    Devuelve la URL de autenticación donde el usuario debe ser redirigido.
    """
    try:
        sso_service = SSOService()
        auth_url = sso_service.get_auth_url()
        
        return {
            "auth_url": auth_url,
            "message": "Redirige al usuario a esta URL para completar la autenticación"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"SSO no disponible: {str(e)}"
        )


@router.get("/sso/callback", summary="Callback del SSO que devuelve el JWT")
def sso_callback(
    code: str = Query(..., description="Código de autorización de Azure AD"),
    db: Session = Depends(get_db)
):
    """
    Endpoint de callback para completar la autenticación SSO.
    Intercambia el código de autorización por un token de acceso y devuelve un JWT.
    """
    try:
        sso_service = SSOService()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"SSO no disponible: {str(e)}"
        )
    
    user_mapping_service = UserMappingServiceImpl(db)
    
    # Intercambia el código por un token
    token_result = sso_service.get_token_from_code(code)
    if not token_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al obtener token de acceso"
        )
    
    # Obtiene información del usuario
    user_info = sso_service.get_user_info(token_result["access_token"])
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al obtener información del usuario"
        )
    
    # Extrae datos del usuario
    username = user_info.get("displayName", "")
    email = user_info.get("mail") or user_info.get("userPrincipalName", "")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo obtener el email del usuario"
        )
    
    # Obtiene el id_api_cliente basado en el email
    id_api_cliente = user_mapping_service.get_api_cliente_id_by_email(email)
    if not id_api_cliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no autorizado para acceder al sistema"
        )
    
    # Crea el JWT con la información requerida
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": username,
            "username": username,
            "email": email,
            "id_api_cliente": id_api_cliente,
            "atisa": True,
            "rol": "admin"
        },
        expires_delta=access_token_expires
    )
    
    # Crea también un refresh token
    refresh_token = create_refresh_token(
        data={
            "sub": username,
            "email": email,
            "id_api_cliente": id_api_cliente,
            "atisa": True,
            "rol": "admin"
        }
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_info": {
            "username": username,
            "email": email,
            "id_api_cliente": id_api_cliente,
            "atisa": True,
            "rol": "admin"
        }
    }


