from fastapi import FastAPI, Depends
from app.infrastructure.api.v1.endpoints import (
    plantilla,
    proceso,
    hito,
    cliente,
    cliente_proceso,
    cliente_proceso_hito,
    plantilla_proceso,
    proceso_hito_maestro,
    admin_api_cliente
)
from app.infrastructure.api.security import verificar_api_key

app = FastAPI(title="API de Procesos de clientes", version="1.0.0")

# Incluir routers con verificación de API key
app.include_router(plantilla.router, dependencies=[Depends(verificar_api_key)])
app.include_router(proceso.router, dependencies=[Depends(verificar_api_key)])
app.include_router(hito.router, dependencies=[Depends(verificar_api_key)])
app.include_router(cliente.router, dependencies=[Depends(verificar_api_key)])
app.include_router(cliente_proceso.router, dependencies=[Depends(verificar_api_key)])
app.include_router(cliente_proceso_hito.router, dependencies=[Depends(verificar_api_key)])
app.include_router(plantilla_proceso.router, dependencies=[Depends(verificar_api_key)])
app.include_router(proceso_hito_maestro.router, dependencies=[Depends(verificar_api_key)])
app.include_router(admin_api_cliente.router)
