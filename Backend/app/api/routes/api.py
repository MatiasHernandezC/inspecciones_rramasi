from fastapi import APIRouter

from app.api.routes import (
    clientes,
    proyectos,
    respuestas_checklist,
    tableros,
    inspecciones,
    checklists,
    fotos,
    informes
)

router = APIRouter()

router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
router.include_router(proyectos.router, prefix="/proyectos", tags=["Proyectos"])
router.include_router(tableros.router, prefix="/tableros", tags=["Tableros"])
router.include_router(inspecciones.router, prefix="/inspecciones", tags=["Inspecciones"])
router.include_router(checklists.router, prefix="/checklists", tags=["Checklists"])
router.include_router(respuestas_checklist.router, prefix="/respuestas_checklists", tags=["RespuestasChecklists"])
router.include_router(fotos.router, prefix="/fotos", tags=["Fotos"])
router.include_router(informes.router, prefix="/informes", tags=["Informes"])
