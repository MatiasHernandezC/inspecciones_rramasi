from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import integrador as crud_integrador
from app.schemas.integrador import IntegradorCreate, IntegradorOut, IntegradorUpdate
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[IntegradorOut])
def listar_integradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_integrador.get_integradores(db, skip, limit)


@router.post("/", response_model=IntegradorOut)
def crear_integrador(integrador: IntegradorCreate, db: Session = Depends(get_db)):
    return crud_integrador.create_integrador(db, integrador)


@router.get("/{integrador_id}", response_model=IntegradorOut)
def obtener_integrador(integrador_id: int, db: Session = Depends(get_db)):
    db_obj = crud_integrador.get_integrador(db, integrador_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Integrador no encontrado")
    return db_obj


@router.put("/{integrador_id}", response_model=IntegradorOut)
def actualizar_integrador(integrador_id: int, integrador: IntegradorUpdate, db: Session = Depends(get_db)):
    db_obj = crud_integrador.update_integrador(db, integrador_id, integrador)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Integrador no encontrado")
    return db_obj


@router.delete("/{integrador_id}")
def eliminar_integrador(integrador_id: int, db: Session = Depends(get_db)):
    db_obj = crud_integrador.delete_integrador(db, integrador_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Integrador no encontrado")
    return {"detail": "Integrador eliminado correctamente"}

