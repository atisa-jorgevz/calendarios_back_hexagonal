from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.db.database import Base

class DocumentoModel(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente_proceso_hito = Column(Integer, ForeignKey("cliente_proceso_hito.id"), nullable=False)
    nombre_documento = Column(String(255), nullable=False)
