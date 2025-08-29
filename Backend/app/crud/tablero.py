from sqlalchemy.orm import Session
from app.models.tablero import Tablero
from app.schemas.tablero import TableroCreate, TableroUpdate

def create_tablero(db: Session, tablero: TableroCreate):
    db_obj = Tablero(**tablero.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_tableros(db: Session, skip: int = 0, limit: int = 100, proyecto: int | None = None):
    q = db.query(Tablero)
    if proyecto is not None:
        q = q.filter(Tablero.id_proyecto == proyecto)
    return q.offset(skip).limit(limit).all()

def get_tablero(db: Session, tablero_id: int):
    return db.query(Tablero).filter(Tablero.id_tablero == tablero_id).first()

def update_tablero(db: Session, tablero_id: int, tablero: TableroUpdate):
    db_obj = get_tablero(db, tablero_id)
    if not db_obj:
        return None
    for key, value in tablero.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_tablero(db: Session, tablero_id: int):
    db_obj = get_tablero(db, tablero_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
