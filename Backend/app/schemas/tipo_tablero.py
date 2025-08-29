from pydantic import BaseModel, ConfigDict
from typing import Optional


class TipoTableroBase(BaseModel):
    nombre: str
    categoria: Optional[str] = None
    activo: Optional[bool] = True


class TipoTableroCreate(TipoTableroBase):
    pass


class TipoTableroUpdate(TipoTableroBase):
    pass


class TipoTableroOut(TipoTableroBase):
    id_tipo: int
    model_config = ConfigDict(from_attributes=True)
