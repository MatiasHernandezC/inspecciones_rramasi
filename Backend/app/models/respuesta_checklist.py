from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class RespuestaChecklist(Base):
    __tablename__ = "respuesta_checklist"

    id_respuesta = Column(Integer, primary_key=True, index=True)
    id_checklist = Column(Integer, ForeignKey("checklist.id_checklist"), nullable=False)
    id_inspeccion = Column(Integer, ForeignKey("inspeccion.id_inspeccion"), nullable=False)
    respuesta = Column(String, nullable=True)
    observacion = Column(Text, nullable=True)

    checklist = relationship("Checklist", back_populates="respuestas")
    inspeccion = relationship("Inspeccion", back_populates="respuestas")
