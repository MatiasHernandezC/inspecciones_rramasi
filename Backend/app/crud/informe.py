from sqlalchemy.orm import Session
from app.models.informe import Informe
from app.schemas.informe import InformeCreate, InformeUpdate

def create_informe(db: Session, informe: InformeCreate):
    db_obj = Informe(**informe.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_informes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Informe).offset(skip).limit(limit).all()

def get_informe(db: Session, informe_id: int):
    return db.query(Informe).filter(Informe.id_informe == informe_id).first()

def update_informe(db: Session, informe_id: int, informe: InformeUpdate):
    db_obj = get_informe(db, informe_id)
    if not db_obj:
        return None
    for key, value in informe.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_informe(db: Session, informe_id: int):
    db_obj = get_informe(db, informe_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
