from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import checklist as crud_checklist
from app.schemas.checklist import ChecklistCreate, ChecklistOut, ChecklistUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChecklistOut)
def crear_checklist(checklist: ChecklistCreate, db: Session = Depends(get_db)):
    return crud_checklist.create_checklist(db, checklist)

@router.get("/", response_model=List[ChecklistOut])
def listar_checklists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_checklist.get_checklists(db, skip, limit)

@router.get("/{checklist_id}", response_model=ChecklistOut)
def obtener_checklist(checklist_id: int, db: Session = Depends(get_db)):
    db_obj = crud_checklist.get_checklist(db, checklist_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Checklist no encontrado")
    return db_obj

@router.put("/{checklist_id}", response_model=ChecklistOut)
def actualizar_checklist(checklist_id: int, checklist: ChecklistUpdate, db: Session = Depends(get_db)):
    db_obj = crud_checklist.update_checklist(db, checklist_id, checklist)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Checklist no encontrado")
    return db_obj

@router.delete("/{checklist_id}")
def eliminar_checklist(checklist_id: int, db: Session = Depends(get_db)):
    db_obj = crud_checklist.delete_checklist(db, checklist_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Checklist no encontrado")
    return {"detail": "Checklist eliminado correctamente"}
