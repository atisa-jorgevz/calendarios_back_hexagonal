from sqlalchemy import Column, Integer, ForeignKey, String
from app.infrastructure.db.database import Base

class DocumentoMetadatoModel(Base):
    __tablename__ = "documento_metadato"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_documento = Column(Integer, ForeignKey("documentos.id"))
    id_metadato = Column(Integer, ForeignKey("metadatos.id"))
    valor = Column(String(255), nullable=False)
