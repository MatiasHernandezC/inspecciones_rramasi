from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import respuesta_checklist as crud_respuesta
from app.schemas.respuesta_checklist import RespuestaChecklistCreate, RespuestaChecklistOut, RespuestaChecklistUpdate
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RespuestaChecklistOut)
def crear_respuesta(respuesta: RespuestaChecklistCreate, db: Session = Depends(get_db)):
    return crud_respuesta.create_respuesta(db, respuesta)

@router.get("/", response_model=List[RespuestaChecklistOut])
def listar_respuestas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_respuesta.get_respuestas(db, skip, limit)

@router.get("/{respuesta_id}", response_model=RespuestaChecklistOut)
def obtener_respuesta(respuesta_id: int, db: Session = Depends(get_db)):
    db_obj = crud_respuesta.get_respuesta(db, respuesta_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    return db_obj

@router.put("/{respuesta_id}", response_model=RespuestaChecklistOut)
def actualizar_respuesta(respuesta_id: int, respuesta: RespuestaChecklistUpdate, db: Session = Depends(get_db)):
    db_obj = crud_respuesta.update_respuesta(db, respuesta_id, respuesta)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    return db_obj

@router.delete("/{respuesta_id}")
def eliminar_respuesta(respuesta_id: int, db: Session = Depends(get_db)):
    db_obj = crud_respuesta.delete_respuesta(db, respuesta_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    return {"detail": "Respuesta eliminada correctamente"}
