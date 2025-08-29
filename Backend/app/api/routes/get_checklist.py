from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.tablero import Tablero
from app.models.plantilla_por_tipo import PlantillaPorTipo
from app.models.checklist_plantilla import ChecklistPlantilla
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist_dynamic import ChecklistResolvedOut, ChecklistItemOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_checklist", response_model=ChecklistResolvedOut)
def get_checklist(tablero: int = Query(..., description="ID de tablero"), db: Session = Depends(get_db)):
    tb = db.query(Tablero).filter(Tablero.id_tablero == tablero).first()
    if not tb:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    if not tb.id_tipo:
        raise HTTPException(status_code=400, detail="El tablero no tiene tipo asociado")

    # Encontrar plantilla vigente para el tipo del tablero
    q = (
        db.query(ChecklistPlantilla)
        .join(PlantillaPorTipo, PlantillaPorTipo.id_plantilla == ChecklistPlantilla.id_plantilla)
        .filter(PlantillaPorTipo.id_tipo == tb.id_tipo, ChecklistPlantilla.vigente == True)  # noqa: E712
        .order_by(ChecklistPlantilla.version.desc())
    )
    plantilla = q.first()
    if not plantilla:
        raise HTTPException(status_code=404, detail="No hay plantilla vigente para el tipo de tablero")

    items = (
        db.query(ChecklistItem)
        .filter(ChecklistItem.id_plantilla == plantilla.id_plantilla)
        .order_by(ChecklistItem.orden.asc())
        .all()
    )

    out_items = []
    for it in items:
        out_items.append(
            ChecklistItemOut(
                id=it.id_item,
                seccion=it.seccion,
                label=it.nombre_item,
                type=it.tipo_item,
                required=bool(it.required),
                rules=it.reglas
            )
        )

    return ChecklistResolvedOut(plantilla_id=plantilla.id_plantilla, version=plantilla.version, items=out_items)

