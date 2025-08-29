from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class TipoTablero(Base):
    __tablename__ = "tipo_tablero"

    id_tipo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

    tableros = relationship("Tablero", back_populates="tipo")

