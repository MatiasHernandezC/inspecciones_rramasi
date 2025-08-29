# schemas/informe.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class InformeBase(BaseModel):
    id_proyecto: int
    id_tablero: int
    id_inspeccion: Optional[int] = None
    numero_informe: Optional[str] = None
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
    model_config = ConfigDict(from_attributes=True)
