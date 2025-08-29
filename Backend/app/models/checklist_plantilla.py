from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ChecklistPlantilla(Base):
    __tablename__ = "checklist_plantilla"

    id_plantilla = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    vigente = Column(Boolean, default=True)

    items = relationship("ChecklistItem", back_populates="plantilla")
    tipos = relationship("PlantillaPorTipo", back_populates="plantilla")

