"""Add extra header fields to inspeccion and seed Legrand test data

Revision ID: 20250901_04_insp_ext_and_seed
Revises: 20250901_03_enforce_types
Create Date: 2025-09-01 14:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20250901_04_insp_ext_and_seed"
down_revision = "20250901_03_enforce_types"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to inspeccion (if absent)
    with op.batch_alter_table("inspeccion") as batch_op:
        try:
            batch_op.add_column(sa.Column("num_solicitud_oc", sa.String(), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column("num_producto", sa.String(), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column("num_serie", sa.String(), nullable=True))
        except Exception:
            pass
        try:
            batch_op.add_column(sa.Column("plano", sa.String(), nullable=True))
        except Exception:
            pass

    # Seed Legrand client + integrador + proyecto + tablero (idempotent)
    bind = op.get_bind()

    # Cliente Legrand
    cli_id = bind.execute(
        sa.text("SELECT id_cliente FROM cliente WHERE nombre = :n"), {"n": "Legrand"}
    ).scalar()
    if not cli_id:
        cli_id = bind.execute(
            sa.text(
                """
                INSERT INTO cliente (nombre, alias, logo_url, contacto, direccion, telefono, email, fecha_creacion)
                VALUES (:nombre, :alias, :logo, :contacto, :dir, :tel, :email, NOW())
                RETURNING id_cliente
                """
            ),
            {
                "nombre": "Legrand",
                "alias": "Legrand",
                "logo": "https://dummyimage.com/160x60/000/fff&text=Legrand",
                "contacto": "Contacto Legrand",
                "dir": "Av. Industrial 123",
                "tel": "+56 2 23456789",
                "email": "contacto@legrand.com",
            },
        ).scalar()

    # Integrador
    int_id = bind.execute(
        sa.text("SELECT id_integrador FROM integrador WHERE nombre = :n"),
        {"n": "ACME Integraciones"},
    ).scalar()
    if not int_id:
        int_id = bind.execute(
            sa.text(
                """
                INSERT INTO integrador (nombre, rut, contacto, telefono, email, direccion, activo)
                VALUES (:nombre, :rut, :contacto, :tel, :email, :dir, TRUE)
                RETURNING id_integrador
                """
            ),
            {
                "nombre": "ACME Integraciones",
                "rut": "76.123.456-7",
                "contacto": "Juan Perez",
                "tel": "+56 9 11111111",
                "email": "juan@acme.cl",
                "dir": "Siempre Viva 123",
            },
        ).scalar()

    # Proyecto
    prj_id = bind.execute(
        sa.text(
            "SELECT id_proyecto FROM proyecto WHERE id_cliente = :c AND nombre = :n"
        ),
        {"c": cli_id, "n": "Proyecto Piloto"},
    ).scalar()
    if not prj_id:
        prj_id = bind.execute(
            sa.text(
                """
                INSERT INTO proyecto (id_cliente, numero, nombre, descripcion, estado, id_integrador, fecha_inicio)
                VALUES (:cl, :num, :nom, :desc, :est, :intg, NOW())
                RETURNING id_proyecto
                """
            ),
            {
                "cl": cli_id,
                "num": "PR-TEST-001",
                "nom": "Proyecto Piloto",
                "desc": "Proyecto de prueba para inspecciones",
                "est": "en_proceso",
                "intg": int_id,
            },
        ).scalar()

    # Tipo de tablero: Autosoportado
    tipo_id = bind.execute(
        sa.text("SELECT id_tipo FROM tipo_tablero WHERE nombre = :n"),
        {"n": "Autosoportado"},
    ).scalar()

    # Tablero
    tbl_id = bind.execute(
        sa.text(
            "SELECT id_tablero FROM tablero WHERE id_proyecto = :p AND codigo_tablero = :cod"
        ),
        {"p": prj_id, "cod": "TAB-TEST-001"},
    ).scalar()
    if not tbl_id:
        tbl_id = bind.execute(
            sa.text(
                """
                INSERT INTO tablero (id_proyecto, id_tipo, codigo_tablero, descripcion, ubicacion)
                VALUES (:p, :t, :cod, :desc, :ubi)
                RETURNING id_tablero
                """
            ),
            {
                "p": prj_id,
                "t": tipo_id,
                "cod": "TAB-TEST-001",
                "desc": "Tablero de prueba autosoportado",
                "ubi": "Planta 1",
            },
        ).scalar()


def downgrade() -> None:
    # Best-effort: no bajamos columnas ni datos de prueba
    pass

