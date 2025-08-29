from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    alias: Optional[str] = None
    logo_url: Optional[str] = None
    contacto: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id_cliente: int
    fecha_creacion: datetime
    model_config = ConfigDict(from_attributes=True)
