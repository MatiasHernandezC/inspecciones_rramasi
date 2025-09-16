from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FotoBase(BaseModel):
    id_cliente: Optional[int] = None
    id_proyecto: Optional[int] = None
    id_tablero: Optional[int] = None
    id_inspeccion: Optional[int] = None
    id_informe: Optional[int] = None
    id_integrador: Optional[int] = None
    id_item: Optional[int] = None
    ruta_archivo: str
    fecha_captura: Optional[datetime] = None
    metadatos: Optional[str] = None

class FotoCreate(FotoBase):
    pass

class FotoUpdate(FotoBase):
    pass

class FotoOut(FotoBase):
    id_foto: int
    model_config = ConfigDict(from_attributes=True)
