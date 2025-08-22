from sqlalchemy.orm import Session
from app.models.checklist import Checklist
from app.schemas.checklist import ChecklistCreate, ChecklistUpdate

def create_checklist(db: Session, checklist: ChecklistCreate):
    db_obj = Checklist(**checklist.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_checklists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Checklist).offset(skip).limit(limit).all()

def get_checklist(db: Session, checklist_id: int):
    return db.query(Checklist).filter(Checklist.id_checklist == checklist_id).first()

def update_checklist(db: Session, checklist_id: int, checklist: ChecklistUpdate):
    db_obj = get_checklist(db, checklist_id)
    if not db_obj:
        return None
    for key, value in checklist.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_checklist(db: Session, checklist_id: int):
    db_obj = get_checklist(db, checklist_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
