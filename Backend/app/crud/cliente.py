from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

# Crear cliente
def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Listar clientes
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

# Obtener cliente por ID
def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

# Actualizar cliente
def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    for key, value in cliente.dict(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Eliminar cliente
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente
