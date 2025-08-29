from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class IntegradorBase(BaseModel):
    nombre: str
    rut: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = True


class IntegradorCreate(IntegradorBase):
    pass


class IntegradorUpdate(IntegradorBase):
    pass


class IntegradorOut(IntegradorBase):
    id_integrador: int
    model_config = ConfigDict(from_attributes=True)
