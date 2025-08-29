# schemas/proyecto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProyectoBase(BaseModel):
    id_cliente: int
    numero: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    id_integrador: Optional[int] = None
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
