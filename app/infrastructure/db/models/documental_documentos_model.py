# app/infrastructure/db/models/documental_documentos_model.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.db.database import Base

class DocumentalDocumentosModel(Base):
    __tablename__ = "documental_documentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(String(9), ForeignKey("clientes.idcliente"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("documental_categorias.id"), nullable=False)
    nombre_documento = Column(String(255), nullable=False)
    original_file_name = Column(String(255), nullable=False)
    stored_file_name = Column(String(255), nullable=False)
