# app/infrastructure/db/models/cliente_proceso_hito_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Date
from sqlalchemy.orm import relationship
from app.infrastructure.db.database import Base

class ClienteProcesoHitoModel(Base):
    __tablename__ = "cliente_proceso_hito"

    id = Column(Integer, primary_key=True, index=True)
    cliente_proceso_id = Column(Integer, ForeignKey("cliente_proceso.id"), nullable=False)
    hito_id = Column(Integer, ForeignKey("proceso_hito_maestro.id"), nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_estado = Column(DateTime, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    cliente_proceso = relationship("ClienteProcesoModel", backref="hitos_cliente")
    hito = relationship("ProcesoHitoMaestroModel", backref="clientes_hito")
