from sqlalchemy.orm import Session
from app.models.inspeccion import Inspeccion
from app.schemas.inspeccion import InspeccionCreate, InspeccionUpdate

def create_inspeccion(db: Session, inspeccion: InspeccionCreate):
    db_obj = Inspeccion(**inspeccion.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_inspecciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Inspeccion).offset(skip).limit(limit).all()

def get_inspeccion(db: Session, inspeccion_id: int):
    return db.query(Inspeccion).filter(Inspeccion.id_inspeccion == inspeccion_id).first()

def update_inspeccion(db: Session, inspeccion_id: int, inspeccion: InspeccionUpdate):
    db_obj = get_inspeccion(db, inspeccion_id)
    if not db_obj:
        return None
    for key, value in inspeccion.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_inspeccion(db: Session, inspeccion_id: int):
    db_obj = get_inspeccion(db, inspeccion_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
