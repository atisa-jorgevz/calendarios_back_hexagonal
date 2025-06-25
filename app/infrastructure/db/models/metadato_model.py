from sqlalchemy import Column, Integer, String
from app.infrastructure.db.database import Base
import enum

class TipoGeneracionEnum(str, enum.Enum):
    AUTO = "auto"
    MANUAL = "manual"

class MetadatoModel(Base):
    __tablename__ = "metadatos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    tipo_generacion = Column(String(10), nullable=False)
    global_ = Column(Integer, default=0) #esto del guion bajo es para evitar conflictos con palabras reservadas.
    activo = Column(Integer, default=1)
