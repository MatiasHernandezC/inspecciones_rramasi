from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Foto(Base):
    __tablename__ = "foto"

    id_foto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=False)
    id_tablero = Column(Integer, ForeignKey("tablero.id_tablero"), nullable=False)
    id_inspeccion = Column(Integer, ForeignKey("inspeccion.id_inspeccion"), nullable=True)
    ruta_archivo = Column(String, nullable=False)
    fecha_captura = Column(DateTime, nullable=True)
    metadatos = Column(Text, nullable=True)

    proyecto = relationship("Proyecto", back_populates="fotos")
    tablero = relationship("Tablero", back_populates="fotos")
    inspeccion = relationship("Inspeccion", back_populates="fotos")
