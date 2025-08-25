from fastapi import APIRouter
from app.api.routes import clientes
from app.api.routes import checklists
from app.api.routes import fotos
from app.api.routes import informes
from app.api.routes import inspecciones
from app.api.routes import proyectos
from app.api.routes import respuestas_checklist
from app.api.routes import tableros

api_router = APIRouter()
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(checklists.router, prefix="/checklists", tags=["checklists"])
api_router.include_router(fotos.router, prefix="/fotos", tags=["fotos"])
api_router.include_router(informes.router, prefix="/informes", tags=["informes"])
api_router.include_router(inspecciones.router, prefix="/inspecciones", tags=["inspecciones"])
api_router.include_router(proyectos.router, prefix="/proyectos", tags=["proyectos"])
api_router.include_router(respuestas_checklist.router, prefix="/respuestas_checklist", tags=["respuestas_checklist"])
api_router.include_router(tableros.router, prefix="/tableros", tags=["tableros"])
