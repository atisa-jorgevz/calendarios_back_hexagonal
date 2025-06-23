from sqlalchemy import Column, Integer, ForeignKey
from app.infrastructure.db.database import Base

class ApiClienteClienteModel(Base):
    __tablename__ = "api_cliente_cliente"

    api_cliente_id = Column(Integer, ForeignKey("api_cliente.id"), primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), primary_key=True)
