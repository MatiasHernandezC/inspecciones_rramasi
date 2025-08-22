from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import tablero as crud_tablero
from app.schemas.tablero import TableroCreate, TableroOut, TableroUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TableroOut)
def crear_tablero(tablero: TableroCreate, db: Session = Depends(get_db)):
    return crud_tablero.create_tablero(db, tablero)

@router.get("/", response_model=List[TableroOut])
def listar_tableros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tablero.get_tableros(db, skip, limit)

@router.get("/{tablero_id}", response_model=TableroOut)
def obtener_tablero(tablero_id: int, db: Session = Depends(get_db)):
    db_obj = crud_tablero.get_tablero(db, tablero_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return db_obj

@router.put("/{tablero_id}", response_model=TableroOut)
def actualizar_tablero(tablero_id: int, tablero: TableroUpdate, db: Session = Depends(get_db)):
    db_obj = crud_tablero.update_tablero(db, tablero_id, tablero)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return db_obj

@router.delete("/{tablero_id}")
def eliminar_tablero(tablero_id: int, db: Session = Depends(get_db)):
    db_obj = crud_tablero.delete_tablero(db, tablero_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return {"detail": "Tablero eliminado correctamente"}
