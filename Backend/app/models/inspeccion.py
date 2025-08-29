from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Inspeccion(Base):
    __tablename__ = "inspeccion"

    id_inspeccion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=False)
    id_tablero = Column(Integer, ForeignKey("tablero.id_tablero"), nullable=False)
    fecha_inspeccion = Column(DateTime, nullable=True)
    inspector = Column(String, nullable=True)
    tipo_visita = Column(Enum('INICIAL', 'MONTAJE', 'FINAL', name='tipo_visita'), nullable=True)
    normativa = Column(String, nullable=True)
    conclusion_calidad = Column(String, nullable=True)
    observaciones = Column(Text, nullable=True)
    estado = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    proyecto = relationship("Proyecto", back_populates="inspecciones")
    tablero = relationship("Tablero", back_populates="inspecciones")
    respuestas = relationship("RespuestaChecklist", back_populates="inspeccion")
    fotos = relationship("Foto", back_populates="inspeccion")
