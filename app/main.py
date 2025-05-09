from fastapi import FastAPI
from app.infrastructure.api.v1.endpoints import proceso
from app.infrastructure.api.v1.endpoints import hito
from app.infrastructure.api.v1.endpoints import proceso_hito_maestro
app = FastAPI()

app.include_router(proceso.router, prefix="/v1")
app.include_router(hito.router, prefix="/v1")
app.include_router(proceso_hito_maestro.router, prefix="/v1")
