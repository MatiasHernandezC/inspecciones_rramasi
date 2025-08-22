from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Tablero(Base):
    __tablename__ = "tablero"

    id_tablero = Column(Integer, primary_key=True, index=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=False)
    codigo_tablero = Column(String, nullable=False)
    tipo_tablero = Column(String, nullable=True)
    descripcion = Column(Text, nullable=True)

    proyecto = relationship("Proyecto", back_populates="tableros")
    inspecciones = relationship("Inspeccion", back_populates="tablero")
    checklists = relationship("Checklist", back_populates="tablero")
    fotos = relationship("Foto", back_populates="tablero")
    informes = relationship("Informe", back_populates="tablero")
