from pydantic import BaseModel
from typing import List, Optional, Any


class ChecklistItemOut(BaseModel):
    id: int
    seccion: Optional[str]
    label: str
    type: str
    required: bool
    rules: Optional[Any] = None


class ChecklistResolvedOut(BaseModel):
    plantilla_id: int
    version: int
    items: List[ChecklistItemOut]

