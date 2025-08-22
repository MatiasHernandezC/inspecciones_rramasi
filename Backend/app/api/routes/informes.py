from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import informe as crud_informe
from app.schemas.informe import InformeCreate, InformeOut, InformeUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InformeOut)
def crear_informe(informe: InformeCreate, db: Session = Depends(get_db)):
    return crud_informe.create_informe(db, informe)

@router.get("/", response_model=List[InformeOut])
def listar_informes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_informe.get_informes(db, skip, limit)

@router.get("/{informe_id}", response_model=InformeOut)
def obtener_informe(informe_id: int, db: Session = Depends(get_db)):
    db_obj = crud_informe.get_informe(db, informe_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return db_obj

@router.put("/{informe_id}", response_model=InformeOut)
def actualizar_informe(informe_id: int, informe: InformeUpdate, db: Session = Depends(get_db)):
    db_obj = crud_informe.update_informe(db, informe_id, informe)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return db_obj

@router.delete("/{informe_id}")
def eliminar_informe(informe_id: int, db: Session = Depends(get_db)):
    db_obj = crud_informe.delete_informe(db, informe_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return {"detail": "Informe eliminado correctamente"}
