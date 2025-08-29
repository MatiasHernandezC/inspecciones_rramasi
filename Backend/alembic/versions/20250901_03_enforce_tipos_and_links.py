"""Enforce tipo_tablero set and relink plantillas

Revision ID: 20250901_03_enforce_tipos_and_links
Revises: 20250901_02_seed_base_checklist
Create Date: 2025-09-01 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20250901_03_enforce_types"
down_revision = "20250901_02_seed_base_checklist"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    deseados = [
        "Autosoportado",
        "Residencial",
        "Murales",
        "Combinados",
        "Banco Condensadores Murales",
        "Banco Condensadores Autosoportados",
    ]

    # Cargar plantillas objetivo
    plantilla_full = bind.execute(
        sa.text(
            "SELECT id_plantilla FROM checklist_plantilla WHERE nombre = :n AND version = 1"
        ),
        {"n": "Base Informe Calidad"},
    ).scalar()
    plantilla_lite = bind.execute(
        sa.text(
            "SELECT id_plantilla FROM checklist_plantilla WHERE nombre = :n AND version = 1"
        ),
        {"n": "Base Informe Calidad Lite"},
    ).scalar()

    # Asegurar que existan los tipos deseados
    existentes = bind.execute(
        sa.text("SELECT nombre, id_tipo FROM tipo_tablero")
    ).fetchall()
    mapa = {n: i for (n, i) in existentes}
    ids = {}
    for n in deseados:
        if n in mapa:
            ids[n] = mapa[n]
        else:
            ids[n] = bind.execute(
                sa.text(
                    "INSERT INTO tipo_tablero (nombre, categoria, activo) VALUES (:n, NULL, TRUE) RETURNING id_tipo"
                ),
                {"n": n},
            ).scalar()

    # Opcional: eliminar tipos basura no deseados (solo si no están referenciados)
    for (n, i) in existentes:
        if n not in deseados:
            # Si no hay referencias en tablero ni plantilla_por_tipo, eliminar
            refs_tab = bind.execute(
                sa.text("SELECT COUNT(*) FROM tablero WHERE id_tipo = :i"), {"i": i}
            ).scalar()
            refs_link = bind.execute(
                sa.text(
                    "SELECT COUNT(*) FROM plantilla_por_tipo WHERE id_tipo = :i"
                ),
                {"i": i},
            ).scalar()
            if (refs_tab or 0) == 0 and (refs_link or 0) == 0:
                bind.execute(sa.text("DELETE FROM tipo_tablero WHERE id_tipo = :i"), {"i": i})

    # Relink: Autosoportado -> full; otros -> lite
    for nombre, id_tipo in ids.items():
        objetivo = plantilla_full if nombre == "Autosoportado" else plantilla_lite
        if objetivo is None:
            continue
        # eliminar vínculos previos a otro objetivo
        bind.execute(
            sa.text(
                "DELETE FROM plantilla_por_tipo WHERE id_tipo = :t AND id_plantilla <> :p"
            ),
            {"t": id_tipo, "p": objetivo},
        )
        # insertar vínculo si no existe
        existe = bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM plantilla_por_tipo WHERE id_tipo = :t AND id_plantilla = :p"
            ),
            {"t": id_tipo, "p": objetivo},
        ).scalar()
        if not existe:
            bind.execute(
                sa.text(
                    "INSERT INTO plantilla_por_tipo (id_tipo, id_plantilla) VALUES (:t, :p)"
                ),
                {"t": id_tipo, "p": objetivo},
            )


def downgrade() -> None:
    # No destructivo; noop
    pass
