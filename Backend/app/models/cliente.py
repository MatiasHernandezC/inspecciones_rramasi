from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    alias = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    contacto = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    proyectos = relationship("Proyecto", back_populates="cliente")
