from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id_cliente: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True
