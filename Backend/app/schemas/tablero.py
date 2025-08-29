# schemas/tablero.py
from pydantic import BaseModel
from typing import Optional

class TableroBase(BaseModel):
    id_proyecto: int
    codigo_tablero: str
    id_tipo: Optional[int] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None

class TableroCreate(TableroBase):
    pass

class TableroUpdate(TableroBase):
    pass

class TableroOut(TableroBase):
    id_tablero: int

    class Config:
        orm_mode = True
