from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.db.database import Base

class ClienteProcesoModel(Base):
    __tablename__ = "cliente_proceso"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(String(9), nullable=True)
    proceso_id = Column(Integer, ForeignKey("proceso.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    mes = Column(Integer, nullable=True)
    anio = Column(Integer, nullable=True)
    anterior_id = Column(Integer, ForeignKey("cliente_proceso.id"), nullable=True)

    # Relaciones
    proceso = relationship("ProcesoModel", backref="cliente_procesos")
    anterior = relationship("ClienteProcesoModel", remote_side=[id])
