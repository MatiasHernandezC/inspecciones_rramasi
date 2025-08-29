# schemas/inspeccion.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class InspeccionBase(BaseModel):
    id_proyecto: int
    id_tablero: int
    fecha_inspeccion: Optional[datetime] = None
    inspector: Optional[str] = None
    tipo_visita: Optional[str] = None  # INICIAL|MONTAJE|FINAL
    normativa: Optional[str] = None
    conclusion_calidad: Optional[str] = None
    observaciones: Optional[str] = None
    estado: Optional[str] = None

class InspeccionCreate(InspeccionBase):
    pass

class InspeccionUpdate(BaseModel):
    id_proyecto: Optional[int] = None
    id_tablero: Optional[int] = None
    fecha_inspeccion: Optional[datetime] = None
    inspector: Optional[str] = None
    tipo_visita: Optional[str] = None
    normativa: Optional[str] = None
    conclusion_calidad: Optional[str] = None
    observaciones: Optional[str] = None
    estado: Optional[str] = None

class InspeccionOut(InspeccionBase):
    id_inspeccion: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
