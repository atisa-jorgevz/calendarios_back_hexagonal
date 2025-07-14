from sqlalchemy import Column, Integer, String, Date, Time
from app.infrastructure.db.database import Base
from sqlalchemy.orm import relationship

class HitoModel(Base):
    __tablename__ = "hito"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    frecuencia = Column(Integer, nullable=False)
    temporalidad = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    hora_limite = Column(Time, nullable=True)
    descripcion = Column(String(255), nullable=True)
    obligatorio = Column(Integer, nullable=False, default=0)  # 0 = No, 1 = Si
    tipo = Column(String(255), nullable=False)

    procesos = relationship("ProcesoHitoMaestroModel", back_populates="hito", cascade="all, delete-orphan")
