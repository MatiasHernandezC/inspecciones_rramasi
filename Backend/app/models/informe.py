from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Informe(Base):
    __tablename__ = "informe"

    id_informe = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=False)
    id_tablero = Column(Integer, ForeignKey("tablero.id_tablero"), nullable=False)
    id_inspeccion = Column(Integer, ForeignKey("inspeccion.id_inspeccion"), nullable=True)
    numero_informe = Column(String, nullable=True)
    tipo_informe = Column(String, nullable=False)
    nombre_archivo = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False)
    fecha_generacion = Column(DateTime, nullable=True)
    estado = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('id_inspeccion', name='uq_informe_inspeccion'),
    )

    proyecto = relationship("Proyecto", back_populates="informes")
    tablero = relationship("Tablero", back_populates="informes")
    inspeccion = relationship("Inspeccion")
