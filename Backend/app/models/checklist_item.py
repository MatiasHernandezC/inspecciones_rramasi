from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_item"

    id_item = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_plantilla = Column(Integer, ForeignKey("checklist_plantilla.id_plantilla"), nullable=False)
    seccion = Column(String, nullable=True)
    nombre_item = Column(String, nullable=False)
    tipo_item = Column(String, nullable=False)  # boolean|number|select|text|foto
    required = Column(Boolean, default=False)
    orden = Column(Integer, nullable=True)
    reglas = Column(String, nullable=True)  # json as text for simplicity

    plantilla = relationship("ChecklistPlantilla", back_populates="items")
    respuestas = relationship("RespuestaChecklist", back_populates="item")
    fotos = relationship("Foto", back_populates="item")

