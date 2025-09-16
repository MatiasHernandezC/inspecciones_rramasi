from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Foto(Base):
    __tablename__ = "foto"

    id_foto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto"), nullable=True)
    id_tablero = Column(Integer, ForeignKey("tablero.id_tablero"), nullable=True)
    id_inspeccion = Column(Integer, ForeignKey("inspeccion.id_inspeccion"), nullable=True)
    id_informe = Column(Integer, ForeignKey("informe.id_informe"), nullable=True)
    id_integrador = Column(Integer, ForeignKey("integrador.id_integrador"), nullable=True)
    id_item = Column(Integer, ForeignKey("checklist_item.id_item"), nullable=True)
    ruta_archivo = Column(String, nullable=False)
    fecha_captura = Column(DateTime, nullable=True)
    metadatos = Column(Text, nullable=True)

    # Relaciones opcionales
    cliente = relationship("Cliente", back_populates="fotos")
    proyecto = relationship("Proyecto", back_populates="fotos")
    tablero = relationship("Tablero", back_populates="fotos")
    inspeccion = relationship("Inspeccion", back_populates="fotos")
    informe = relationship("Informe", back_populates="fotos")
    integrador = relationship("Integrador", back_populates="fotos")
    item = relationship("ChecklistItem", back_populates="fotos")
