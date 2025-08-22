from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import cliente as crud_cliente
from app.schemas.cliente import ClienteCreate, ClienteOut, ClienteUpdate
from app.db.session import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear cliente
@router.post("/", response_model=ClienteOut)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crud_cliente.create_cliente(db, cliente)

# Listar clientes
@router.get("/", response_model=List[ClienteOut])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_cliente.get_clientes(db, skip, limit)

# Obtener cliente por ID
@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# Actualizar cliente
@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.update_cliente(db, cliente_id, cliente)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# Eliminar cliente
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.delete_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"detail": "Cliente eliminado correctamente"}
