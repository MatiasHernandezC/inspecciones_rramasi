# schemas/respuesta_checklist.py
from pydantic import BaseModel
from typing import Optional

class RespuestaChecklistBase(BaseModel):
    id_checklist: int
    id_inspeccion: int
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
