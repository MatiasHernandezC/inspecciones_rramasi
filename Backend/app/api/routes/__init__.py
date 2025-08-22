from fastapi import APIRouter
from app.api.routes import clientes  # importa tu archivo de endpoints

api_router = APIRouter()
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
