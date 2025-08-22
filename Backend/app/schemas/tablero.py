# schemas/tablero.py
from pydantic import BaseModel
from typing import Optional

class TableroBase(BaseModel):
    id_proyecto: int
    codigo_tablero: str
    tipo_tablero: Optional[str] = None
    descripcion: Optional[str] = None

class TableroCreate(TableroBase):
    pass

class TableroUpdate(TableroBase):
    pass

class TableroOut(TableroBase):
    id_tablero: int

    class Config:
        orm_mode = True
