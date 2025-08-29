from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate

def create_proyecto(db: Session, proyecto: ProyectoCreate):
    db_obj = Proyecto(**proyecto.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_proyectos(db: Session, skip: int = 0, limit: int = 100, cliente: int | None = None):
    q = db.query(Proyecto)
    if cliente is not None:
        q = q.filter(Proyecto.id_cliente == cliente)
    return q.offset(skip).limit(limit).all()

def get_proyecto(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id_proyecto == proyecto_id).first()

def update_proyecto(db: Session, proyecto_id: int, proyecto: ProyectoUpdate):
    db_obj = get_proyecto(db, proyecto_id)
    if not db_obj:
        return None
    for key, value in proyecto.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_proyecto(db: Session, proyecto_id: int):
    db_obj = get_proyecto(db, proyecto_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
