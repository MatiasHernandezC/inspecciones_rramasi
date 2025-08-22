from app.db.base_class import Base
from app.db.session import engine
from app.models.cliente import Cliente  # importa todos los modelos

Base.metadata.create_all(bind=engine)
print("Tablas creadas")
