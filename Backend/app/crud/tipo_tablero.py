from sqlalchemy.orm import Session
from app.models.tipo_tablero import TipoTablero
from app.schemas.tipo_tablero import TipoTableroCreate, TipoTableroUpdate


def create_tipo_tablero(db: Session, obj: TipoTableroCreate):
    db_obj = TipoTablero(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_tipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TipoTablero).offset(skip).limit(limit).all()


def get_tipo(db: Session, tipo_id: int):
    return db.query(TipoTablero).filter(TipoTablero.id_tipo == tipo_id).first()


def update_tipo(db: Session, tipo_id: int, obj: TipoTableroUpdate):
    db_obj = get_tipo(db, tipo_id)
    if not db_obj:
        return None
    for key, value in obj.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_tipo(db: Session, tipo_id: int):
    db_obj = get_tipo(db, tipo_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj

