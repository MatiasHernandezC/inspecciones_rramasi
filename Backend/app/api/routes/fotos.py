from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import foto as crud_foto
from app.schemas.foto import FotoCreate, FotoOut, FotoUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FotoOut)
def crear_foto(foto: FotoCreate, db: Session = Depends(get_db)):
    return crud_foto.create_foto(db, foto)

@router.get("/", response_model=List[FotoOut])
def listar_fotos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_foto.get_fotos(db, skip, limit)

@router.get("/{foto_id}", response_model=FotoOut)
def obtener_foto(foto_id: int, db: Session = Depends(get_db)):
    db_obj = crud_foto.get_foto(db, foto_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_obj

@router.put("/{foto_id}", response_model=FotoOut)
def actualizar_foto(foto_id: int, foto: FotoUpdate, db: Session = Depends(get_db)):
    db_obj = crud_foto.update_foto(db, foto_id, foto)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return db_obj

@router.delete("/{foto_id}")
def eliminar_foto(foto_id: int, db: Session = Depends(get_db)):
    db_obj = crud_foto.delete_foto(db, foto_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return {"detail": "Foto eliminada correctamente"}
