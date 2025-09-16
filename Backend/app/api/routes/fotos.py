from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil, uuid
from typing import Optional
from datetime import datetime
from typing import List
from fastapi import Query
from app.crud import foto as crud_foto
from app.schemas.foto import FotoCreate, FotoOut
from app.db.session import SessionLocal

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent.parent / "media/fotos"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/", response_model=List[FotoOut])
def listar_fotos(
    id_inspeccion: Optional[int] = Query(None),
    id_cliente: Optional[int] = Query(None),
    id_proyecto: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(crud_foto.Foto)

    if id_inspeccion:
        query = query.filter(crud_foto.Foto.id_inspeccion == id_inspeccion)
    if id_cliente:
        query = query.filter(crud_foto.Foto.id_cliente == id_cliente)
    if id_proyecto:
        query = query.filter(crud_foto.Foto.id_proyecto == id_proyecto)

    return query.all()

@router.post("/upload", response_model=FotoOut)
def upload_foto(
    file: UploadFile = File(...),
    id_cliente: Optional[int] = Form(None),
    id_proyecto: Optional[int] = Form(None),
    id_tablero: Optional[int] = Form(None),
    id_inspeccion: Optional[int] = Form(None),
    id_informe: Optional[int] = Form(None),
    id_integrador: Optional[int] = Form(None),
    id_item: Optional[int] = Form(None),
    fecha_captura: Optional[datetime] = Form(None),
    db: Session = Depends(get_db),
):
    if not (id_cliente or id_proyecto or id_tablero or id_inspeccion or id_informe or id_integrador):
        raise HTTPException(status_code=400, detail="Debe asociar la foto a algún contexto")

    # Carpeta general por proyecto o cliente (evitar duplicar)
    folder_name = f"cliente_{id_cliente}" if id_cliente else f"proyecto_{id_proyecto}" if id_proyecto else "otros"
    folder = UPLOAD_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)

    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = folder / unique_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    url = f"/media/fotos/{folder_name}/{unique_name}"

    foto_in = FotoCreate(
        id_cliente=id_cliente,
        id_proyecto=id_proyecto,
        id_tablero=id_tablero,
        id_inspeccion=id_inspeccion,
        id_informe=id_informe,
        id_integrador=id_integrador,
        id_item=id_item,
        ruta_archivo=url,
        fecha_captura=fecha_captura or datetime.utcnow()
    )

    return crud_foto.create_foto(db, foto_in)
    