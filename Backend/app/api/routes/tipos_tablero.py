from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import tipo_tablero as crud_tipo
from app.schemas.tipo_tablero import TipoTableroCreate, TipoTableroOut, TipoTableroUpdate
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[TipoTableroOut])
def listar_tipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tipo.get_tipos(db, skip, limit)


@router.post("/", response_model=TipoTableroOut)
def crear_tipo(tipo: TipoTableroCreate, db: Session = Depends(get_db)):
    return crud_tipo.create_tipo_tablero(db, tipo)


@router.get("/{tipo_id}", response_model=TipoTableroOut)
def obtener_tipo(tipo_id: int, db: Session = Depends(get_db)):
    db_obj = crud_tipo.get_tipo(db, tipo_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tipo de tablero no encontrado")
    return db_obj


@router.put("/{tipo_id}", response_model=TipoTableroOut)
def actualizar_tipo(tipo_id: int, tipo: TipoTableroUpdate, db: Session = Depends(get_db)):
    db_obj = crud_tipo.update_tipo(db, tipo_id, tipo)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tipo de tablero no encontrado")
    return db_obj


@router.delete("/{tipo_id}")
def eliminar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    db_obj = crud_tipo.delete_tipo(db, tipo_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tipo de tablero no encontrado")
    return {"detail": "Tipo de tablero eliminado correctamente"}

