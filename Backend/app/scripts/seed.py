from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.db.session import SQLALCHEMY_DATABASE_URL
from app.models.cliente import Cliente
from app.models.integrador import Integrador
from app.models.proyecto import Proyecto
from app.models.tipo_tablero import TipoTablero
from app.models.tablero import Tablero
from app.models.checklist_plantilla import ChecklistPlantilla
from app.models.checklist_item import ChecklistItem
from app.models.plantilla_por_tipo import PlantillaPorTipo


def get_engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)


def get_or_create(session: Session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance, True


def run():
    engine = get_engine()
    with Session(bind=engine) as session:
        # Clientes
        legrand, _ = get_or_create(session, Cliente, nombre="Legrand", alias="Legrand", logo_url="https://dummyimage.com/160x60/000/fff&text=Legrand")
        schneider, _ = get_or_create(session, Cliente, nombre="Schneider", alias="Schneider", logo_url="https://dummyimage.com/160x60/1e293b/fff&text=Schneider")

        # Integradores
        intg, _ = get_or_create(session, Integrador, nombre="ACME Integraciones", rut="76.123.456-7", contacto="Juan Perez", telefono="+56 9 1111 1111", email="juan@acme.cl", direccion="Av. Siempre Viva 123", activo=True)

        # Tipos de Tablero
        t_res, _ = get_or_create(session, TipoTablero, nombre="Residencial", categoria="Tablero", activo=True)
        t_mural, _ = get_or_create(session, TipoTablero, nombre="Mural", categoria="Tablero", activo=True)

        # Proyecto
        prj, _ = get_or_create(session, Proyecto, id_cliente=legrand.id_cliente, numero="PR-2025-001", nombre="Edificio Central", descripcion="Proyecto piloto", estado="en_proceso", id_integrador=intg.id_integrador, fecha_inicio=datetime.utcnow())

        # Tableros
        tb1, _ = get_or_create(session, Tablero, id_proyecto=prj.id_proyecto, id_tipo=t_mural.id_tipo, codigo_tablero="TAB-001", descripcion="Tablero principal", ubicacion="Sala eléctrica")
        tb2, _ = get_or_create(session, Tablero, id_proyecto=prj.id_proyecto, id_tipo=t_res.id_tipo, codigo_tablero="TAB-002", descripcion="Tablero secundario", ubicacion="Oficina 101")

        # Plantilla para Mural
        pl, created_pl = get_or_create(session, ChecklistPlantilla, nombre="Mural v1", descripcion="Checklist base Mural", version=1, vigente=True)

        # Vincular plantilla a tipos si no existe (Mural y Residencial)
        def ensure_link(tipo_id, plantilla_id):
            link = (
                session.query(PlantillaPorTipo)
                .filter(
                    PlantillaPorTipo.id_tipo == tipo_id,
                    PlantillaPorTipo.id_plantilla == plantilla_id,
                )
                .first()
            )
            if not link:
                session.add(PlantillaPorTipo(id_tipo=tipo_id, id_plantilla=plantilla_id))
                session.commit()

        ensure_link(t_mural.id_tipo, pl.id_plantilla)
        ensure_link(t_res.id_tipo, pl.id_plantilla)

        # Items de la plantilla (idempotente por nombre dentro de plantilla)
        def upsert_item(seccion, nombre, tipo, required=False, orden=None, reglas=None):
            q = session.query(ChecklistItem).filter_by(id_plantilla=pl.id_plantilla, nombre_item=nombre)
            obj = q.first()
            if obj:
                return obj
            obj = ChecklistItem(id_plantilla=pl.id_plantilla, seccion=seccion, nombre_item=nombre, tipo_item=tipo, required=required, orden=orden, reglas=reglas)
            session.add(obj)
            session.commit()
            return obj

        upsert_item("Seguridad", "Protección diferencial", "boolean", True, 1, None)
        upsert_item("Seguridad", "Sensibilidad (mA)", "number", True, 2, '{"min":10,"max":500}')
        upsert_item("Etiquetado", "Rotulado de circuitos", "select", True, 3, '{"options":["OK","Observación","No aplica"]}')

        print("Seed completado:")
        print(f"  Clientes: {legrand.nombre}, {schneider.nombre}")
        print(f"  Integrador: {intg.nombre}")
        print(f"  Proyecto: {prj.nombre}")
        print(f"  Tableros: {tb1.codigo_tablero}, {tb2.codigo_tablero}")
        print(f"  Plantilla: {pl.nombre} vinculada a tipo '{t_mural.nombre}' y '{t_res.nombre}'")


if __name__ == "__main__":
    run()
