from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Integrador(Base):
    __tablename__ = "integrador"

    id_integrador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    rut = Column(String, nullable=True)
    contacto = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

    proyectos = relationship("Proyecto", back_populates="integrador")
    fotos = relationship("Foto", back_populates="integrador")

