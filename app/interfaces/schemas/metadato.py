from pydantic import BaseModel, Field

class MetadatoCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    tipo_generacion: str
    global_: int = Field(..., alias="global")
    activo: int = 1

class MetadatoRead(MetadatoCreate):
    id: int

    class Config:
        orm_mode = True
        populate_by_name = True
    
class MetadatoUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None
    tipo_generacion: str
    global_: int = Field(..., alias="global")
    activo: int = 1

class MetadatoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    tipo_generacion: str
    global_: int
    activo: int

