# schemas/foto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FotoBase(BaseModel):
    id_proyecto: int
    id_tablero: int
    id_inspeccion: Optional[int] = None
    ruta_archivo: str
    fecha_captura: Optional[datetime] = None
    metadatos: Optional[str] = None

class FotoCreate(FotoBase):
    pass

class FotoUpdate(FotoBase):
    pass

class FotoOut(FotoBase):
    id_foto: int

    class Config:
        orm_mode = True
