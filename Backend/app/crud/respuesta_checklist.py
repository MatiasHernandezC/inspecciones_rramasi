from sqlalchemy.orm import Session
from app.models.respuesta_checklist import RespuestaChecklist
from app.schemas.respuesta_checklist import RespuestaChecklistCreate, RespuestaChecklistUpdate

def create_respuesta(db: Session, respuesta: RespuestaChecklistCreate):
    db_obj = RespuestaChecklist(**respuesta.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_respuestas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RespuestaChecklist).offset(skip).limit(limit).all()

def get_respuesta(db: Session, respuesta_id: int):
    return db.query(RespuestaChecklist).filter(RespuestaChecklist.id_respuesta == respuesta_id).first()

def update_respuesta(db: Session, respuesta_id: int, respuesta: RespuestaChecklistUpdate):
    db_obj = get_respuesta(db, respuesta_id)
    if not db_obj:
        return None
    for key, value in respuesta.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_respuesta(db: Session, respuesta_id: int):
    db_obj = get_respuesta(db, respuesta_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
