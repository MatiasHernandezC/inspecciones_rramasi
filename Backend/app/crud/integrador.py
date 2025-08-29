from sqlalchemy.orm import Session
from app.models.integrador import Integrador
from app.schemas.integrador import IntegradorCreate, IntegradorUpdate


def create_integrador(db: Session, integrador: IntegradorCreate):
    db_obj = Integrador(**integrador.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_integradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Integrador).offset(skip).limit(limit).all()


def get_integrador(db: Session, integrador_id: int):
    return db.query(Integrador).filter(Integrador.id_integrador == integrador_id).first()


def update_integrador(db: Session, integrador_id: int, integrador: IntegradorUpdate):
    db_obj = get_integrador(db, integrador_id)
    if not db_obj:
        return None
    for key, value in integrador.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_integrador(db: Session, integrador_id: int):
    db_obj = get_integrador(db, integrador_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj

