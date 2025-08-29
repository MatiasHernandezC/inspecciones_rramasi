from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class PlantillaPorTipo(Base):
    __tablename__ = "plantilla_por_tipo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_tipo = Column(Integer, ForeignKey("tipo_tablero.id_tipo"), nullable=False)
    id_plantilla = Column(Integer, ForeignKey("checklist_plantilla.id_plantilla"), nullable=False)

    __table_args__ = (
        UniqueConstraint('id_tipo', 'id_plantilla', name='uq_tipo_plantilla'),
    )

    tipo = relationship("TipoTablero")
    plantilla = relationship("ChecklistPlantilla", back_populates="tipos")

