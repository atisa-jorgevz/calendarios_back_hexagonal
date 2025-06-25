from fastapi import FastAPI, Depends
from app.interfaces.api.v1.endpoints import (
    plantilla,
    proceso,
    hito,
    cliente,
    cliente_proceso,
    cliente_proceso_hito,
    plantilla_proceso,
    proceso_hito_maestro,
    admin_api_cliente,
    metadato,
)
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.api import auth_routes
from app.interfaces.api.security.auth import get_current_user



origins = [
    "http://localhost:3000",  # frontend local
    "http://127.0.0.1:3000",
    "http://10.150.22.15:5173",  # si accedes desde IP local
    # "https://tu-front-en-produccion.com",  <-- añade si tienes front desplegado
]

app = FastAPI(title="API de Procesos de clientes", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Puedes limitarlo a ["GET", "POST", ...] si quieres
    allow_headers=["*"],  # Puedes limitar a ["x_api_key", "Content-Type"]
)

app.include_router(auth_routes.router)
app.include_router(admin_api_cliente.router)
# Incluir routers con verificación de API key
app.include_router(plantilla.router, dependencies=[Depends(get_current_user)])
app.include_router(proceso.router, dependencies=[Depends(get_current_user)])
app.include_router(hito.router, dependencies=[Depends(get_current_user)])
app.include_router(cliente.router, dependencies=[Depends(get_current_user)])
app.include_router(cliente_proceso.router, dependencies=[Depends(get_current_user)])
app.include_router(cliente_proceso_hito.router, dependencies=[Depends(get_current_user)])
app.include_router(plantilla_proceso.router, dependencies=[Depends(get_current_user)])
app.include_router(proceso_hito_maestro.router, dependencies=[Depends(get_current_user)])
app.include_router(metadato.router, dependencies=[Depends(get_current_user)])


