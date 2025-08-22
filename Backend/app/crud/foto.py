from sqlalchemy.orm import Session
from app.models.foto import Foto
from app.schemas.foto import FotoCreate, FotoUpdate

def create_foto(db: Session, foto: FotoCreate):
    db_obj = Foto(**foto.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_fotos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Foto).offset(skip).limit(limit).all()

def get_foto(db: Session, foto_id: int):
    return db.query(Foto).filter(Foto.id_foto == foto_id).first()

def update_foto(db: Session, foto_id: int, foto: FotoUpdate):
    db_obj = get_foto(db, foto_id)
    if not db_obj:
        return None
    for key, value in foto.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_foto(db: Session, foto_id: int):
    db_obj = get_foto(db, foto_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
