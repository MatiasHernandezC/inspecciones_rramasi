from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import proyecto as crud_proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProyectoOut)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    return crud_proyecto.create_proyecto(db, proyecto)

@router.get("/", response_model=List[ProyectoOut])
def listar_proyectos(skip: int = 0, limit: int = 100, cliente: int | None = None, db: Session = Depends(get_db)):
    return crud_proyecto.get_proyectos(db, skip, limit, cliente)

@router.get("/{proyecto_id}", response_model=ProyectoOut)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_obj = crud_proyecto.get_proyecto(db, proyecto_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_obj

@router.put("/{proyecto_id}", response_model=ProyectoOut)
def actualizar_proyecto(proyecto_id: int, proyecto: ProyectoUpdate, db: Session = Depends(get_db)):
    db_obj = crud_proyecto.update_proyecto(db, proyecto_id, proyecto)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_obj

@router.delete("/{proyecto_id}")
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_obj = crud_proyecto.delete_proyecto(db, proyecto_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"detail": "Proyecto eliminado correctamente"}
