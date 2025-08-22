from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import inspeccion as crud_inspeccion
from app.schemas.inspeccion import InspeccionCreate, InspeccionOut, InspeccionUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InspeccionOut)
def crear_inspeccion(inspeccion: InspeccionCreate, db: Session = Depends(get_db)):
    return crud_inspeccion.create_inspeccion(db, inspeccion)

@router.get("/", response_model=List[InspeccionOut])
def listar_inspecciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_inspeccion.get_inspecciones(db, skip, limit)

@router.get("/{inspeccion_id}", response_model=InspeccionOut)
def obtener_inspeccion(inspeccion_id: int, db: Session = Depends(get_db)):
    db_obj = crud_inspeccion.get_inspeccion(db, inspeccion_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return db_obj

@router.put("/{inspeccion_id}", response_model=InspeccionOut)
def actualizar_inspeccion(inspeccion_id: int, inspeccion: InspeccionUpdate, db: Session = Depends(get_db)):
    db_obj = crud_inspeccion.update_inspeccion(db, inspeccion_id, inspeccion)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return db_obj

@router.delete("/{inspeccion_id}")
def eliminar_inspeccion(inspeccion_id: int, db: Session = Depends(get_db)):
    db_obj = crud_inspeccion.delete_inspeccion(db, inspeccion_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return {"detail": "Inspección eliminada correctamente"}
