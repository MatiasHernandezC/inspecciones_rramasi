# schemas/informe.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InformeBase(BaseModel):
    id_proyecto: int
    id_tablero: int
    tipo_informe: Optional[str] = None
    nombre_archivo: Optional[str] = None
    ruta_archivo: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
    estado: Optional[str] = None

class InformeCreate(InformeBase):
    pass

class InformeUpdate(InformeBase):
    pass

class InformeOut(InformeBase):
    id_informe: int

    class Config:
        orm_mode = True
