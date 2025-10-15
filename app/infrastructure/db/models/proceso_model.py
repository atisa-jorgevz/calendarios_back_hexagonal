from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.infrastructure.db.database import Base




class ProcesoModel(Base):
    __tablename__ = "proceso"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    frecuencia = Column(Integer, nullable=False)
    temporalidad = Column(String(50), nullable=False)
    inicia_dia_1 = Column(Integer, nullable=False, default=0)
    habilitado = Column(Boolean, nullable=False, default=True)
    hitos = relationship("ProcesoHitoMaestroModel", back_populates="proceso", cascade="all, delete-orphan")
    plantillas = relationship("PlantillaProcesoModel", back_populates="proceso", cascade="all, delete-orphan")
