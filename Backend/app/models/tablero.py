from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Tablero(Base):
    __tablename__ = "tablero"

    id_tablero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=False)
    codigo_tablero = Column(String, nullable=False)
    id_tipo = Column(Integer, ForeignKey("tipo_tablero.id_tipo"), nullable=True)
    descripcion = Column(Text, nullable=True)
    ubicacion = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('id_proyecto', 'codigo_tablero', name='uq_tablero_proyecto_codigo'),
    )

    proyecto = relationship("Proyecto", back_populates="tableros")
    tipo = relationship("TipoTablero", back_populates="tableros")
    inspecciones = relationship("Inspeccion", back_populates="tablero")
    fotos = relationship("Foto", back_populates="tablero")
    informes = relationship("Informe", back_populates="tablero")
