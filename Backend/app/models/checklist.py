from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Checklist(Base):
    __tablename__ = "checklist"

    id_checklist = Column(Integer, primary_key=True, index=True)
    id_tablero = Column(Integer, ForeignKey("tablero.id_tablero"), nullable=False)
    nombre_item = Column(String, nullable=False)
    tipo_item = Column(String, nullable=True)
    orden = Column(Integer, nullable=True)
    valor_default = Column(String, nullable=True)
