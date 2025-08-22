# schemas/proyecto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProyectoBase(BaseModel):
    id_cliente: int
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(ProyectoBase):
    pass

class ProyectoOut(ProyectoBase):
    id_proyecto: int

    class Config:
        orm_mode = True
