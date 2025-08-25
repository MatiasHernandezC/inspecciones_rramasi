from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Proyecto(Base):
    __tablename__ = "proyecto"

    id_proyecto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String, nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)

    cliente = relationship("Cliente", back_populates="proyectos")
    tableros = relationship("Tablero", back_populates="proyecto")
    inspecciones = relationship("Inspeccion", back_populates="proyecto")
    informes = relationship("Informe", back_populates="proyecto")
    fotos = relationship("Foto", back_populates="proyecto")
