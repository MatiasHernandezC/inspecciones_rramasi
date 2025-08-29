# schemas/checklist.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ChecklistBase(BaseModel):
    id_tablero: int
    nombre_item: str
    tipo_item: Optional[str] = None
    orden: Optional[int] = None
    valor_default: Optional[str] = None

class ChecklistCreate(ChecklistBase):
    pass

class ChecklistUpdate(ChecklistBase):
    pass

class ChecklistOut(ChecklistBase):
    id_checklist: int
    model_config = ConfigDict(from_attributes=True)
