from fastapi import FastAPI
from app.infrastructure.api.v1.endpoints import proceso
from app.infrastructure.api.v1.endpoints import hito
from app.infrastructure.api.v1.endpoints import proceso_hito_maestro
from app.infrastructure.api.v1.endpoints import plantilla
from app.infrastructure.api.v1.endpoints import plantilla_proceso
from app.infrastructure.api.v1.endpoints import cliente
from app.infrastructure.api.v1.endpoints import cliente_proceso
from app.infrastructure.api.v1.endpoints import cliente_proceso_hito

app = FastAPI()

app.include_router(proceso.router, prefix="/v1")
app.include_router(hito.router, prefix="/v1")
app.include_router(proceso_hito_maestro.router, prefix="/v1")
app.include_router(plantilla.router, prefix="/v1")
app.include_router(plantilla_proceso.router, prefix="/v1", tags=["PlantillaProceso"])
app.include_router(cliente.router, prefix="/v1", tags=["Cliente"])
app.include_router(cliente_proceso.router, prefix="/v1", tags=["ClienteProceso"])
app.include_router(cliente_proceso_hito.router, prefix="/v1", tags=["ClienteProcesoHito"])

