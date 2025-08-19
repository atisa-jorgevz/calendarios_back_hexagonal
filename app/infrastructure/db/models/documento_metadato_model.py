from sqlalchemy import Column, Integer, ForeignKey, Text
from app.infrastructure.db.database import Base

class DocumentoMetadatoModel(Base):
    __tablename__ = "documento_metadato"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_documento = Column(Integer, ForeignKey("documentos.id"))
    metadatos = Column(Text)
