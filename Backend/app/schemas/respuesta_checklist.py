# schemas/respuesta_checklist.py
from pydantic import BaseModel
from typing import Optional

class RespuestaChecklistBase(BaseModel):
    id_inspeccion: int
    id_item: int
    respuesta: Optional[str] = None
    observacion: Optional[str] = None

class RespuestaChecklistCreate(RespuestaChecklistBase):
    pass

class RespuestaChecklistUpdate(RespuestaChecklistBase):
    pass

class RespuestaChecklistOut(RespuestaChecklistBase):
    id_respuesta: int

    class Config:
        orm_mode = True
