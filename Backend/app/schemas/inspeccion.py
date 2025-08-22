# schemas/inspeccion.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InspeccionBase(BaseModel):
    id_proyecto: int
    id_tablero: int
    fecha_inspeccion: Optional[datetime] = None
    inspector: Optional[str] = None
    conclusion_calidad: Optional[str] = None
    observaciones: Optional[str] = None
    estado: Optional[str] = None

class InspeccionCreate(InspeccionBase):
    pass

class InspeccionUpdate(InspeccionBase):
    pass

class InspeccionOut(InspeccionBase):
    id_inspeccion: int

    class Config:
        orm_mode = True
