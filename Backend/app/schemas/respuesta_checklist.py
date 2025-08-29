# schemas/respuesta_checklist.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

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
    model_config = ConfigDict(from_attributes=True)


class RespuestaItemIn(BaseModel):
    id_item: int
    respuesta: Optional[str] = None
    observacion: Optional[str] = None


class RespuestasBulkIn(BaseModel):
    respuestas: List[RespuestaItemIn]
