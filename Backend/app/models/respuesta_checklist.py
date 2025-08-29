from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class RespuestaChecklist(Base):
    __tablename__ = "respuesta_checklist"

    id_respuesta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_inspeccion = Column(Integer, ForeignKey("inspeccion.id_inspeccion"), nullable=False)
    id_item = Column(Integer, ForeignKey("checklist_item.id_item"), nullable=False)
    respuesta = Column(String, nullable=True)
    observacion = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint('id_inspeccion', 'id_item', name='uq_respuesta_inspeccion_item'),
    )

    item = relationship("ChecklistItem", back_populates="respuestas")
    inspeccion = relationship("Inspeccion", back_populates="respuestas")
