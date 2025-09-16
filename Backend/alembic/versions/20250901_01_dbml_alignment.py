"""Align schema to new DBML design (idempotent)

Revision ID: 20250901_01_dbml_alignment
Revises:
Create Date: 2025-09-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '20250901_01_dbml_alignment'
down_revision = None
branch_labels = None
depends_on = None

# ENUM reutilizable (no crear el tipo de nuevo si ya existe)
tipo_visita_enum = postgresql.ENUM(
    'INICIAL', 'MONTAJE', 'FINAL',
    name='tipo_visita',
    create_type=False  # <- clave: evita CREATE TYPE duplicado
)
# --- Helpers ---------------------------------------------------------------

def inspector():
    bind = op.get_bind()
    return sa.inspect(bind)

def has_table(name):
    return name in inspector().get_table_names()

def has_column(table, column):
    insp = inspector()
    if table not in insp.get_table_names():
        return False
    cols = [c['name'] for c in insp.get_columns(table)]
    return column in cols

def create_table_if_absent(name, *columns, **kwargs):
    if not has_table(name):
        op.create_table(name, *columns, **kwargs)

def add_column_if_absent(table, column):
    # column is a sa.Column(...)
    if not has_column(table, column.name):
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(column)

def _has_unique(constraint_name, table):
    insp = inspector()
    try:
        uqs = insp.get_unique_constraints(table)
    except Exception:
        return False
    return any(uq.get("name") == constraint_name for uq in uqs)


def add_unique_if_absent(constraint_name, table, columns):
    if not _has_unique(constraint_name, table):
        op.create_unique_constraint(constraint_name, table, columns)

def _has_fk(constraint_name, source_table, referent_table, local_cols):
    insp = inspector()
    try:
        fks = insp.get_foreign_keys(source_table)
    except Exception:
        return False
    if constraint_name:
        return any(fk.get("name") == constraint_name for fk in fks)
    # Coincidencia por especificación
    for fk in fks:
        if fk.get("referred_table") == referent_table and fk.get("constrained_columns") == local_cols:
            return True
    return False


def add_fk_if_absent(constraint_name, source_table, referent_table, local_cols, remote_cols, **kw):
    if not _has_fk(constraint_name, source_table, referent_table, local_cols):
        op.create_foreign_key(constraint_name, source_table, referent_table, local_cols, remote_cols, **kw)

# --- Upgrade ---------------------------------------------------------------

def upgrade() -> None:
    # 0) ENUM tipo_visita (Postgres)
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_visita') THEN
            CREATE TYPE tipo_visita AS ENUM ('INICIAL','MONTAJE','FINAL');
        END IF;
    END
    $$;
    """)

    # 1) Tablas puramente nuevas (crear si faltan)
    create_table_if_absent(
        'integrador',
        sa.Column('id_integrador', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('rut', sa.String(), nullable=True),
        sa.Column('contacto', sa.String(), nullable=True),
        sa.Column('telefono', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('direccion', sa.String(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=True, server_default=sa.true()),
    )

    create_table_if_absent(
        'tipo_tablero',
        sa.Column('id_tipo', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('categoria', sa.String(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=True, server_default=sa.true()),
    )

    create_table_if_absent(
        'checklist_plantilla',
        sa.Column('id_plantilla', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('vigente', sa.Boolean(), nullable=True, server_default=sa.true()),
    )

    create_table_if_absent(
        'checklist_item',
        sa.Column('id_item', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_plantilla', sa.Integer(), nullable=False),
        sa.Column('seccion', sa.String(), nullable=True),
        sa.Column('nombre_item', sa.String(), nullable=False),
        sa.Column('tipo_item', sa.String(), nullable=False),
        sa.Column('required', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('orden', sa.Integer(), nullable=True),
        sa.Column('reglas', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['id_plantilla'], ['checklist_plantilla.id_plantilla'])
    )

    create_table_if_absent(
        'plantilla_por_tipo',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_tipo', sa.Integer(), nullable=False),
        sa.Column('id_plantilla', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_tipo'], ['tipo_tablero.id_tipo']),
        sa.ForeignKeyConstraint(['id_plantilla'], ['checklist_plantilla.id_plantilla'])
    )
    add_unique_if_absent('uq_tipo_plantilla', 'plantilla_por_tipo', ['id_tipo', 'id_plantilla'])

    # 2) Tablas base que podrían estar o no: crear si faltan, si existen agregar columnas

    # CLIENTE
    if not has_table('cliente'):
        op.create_table(
            'cliente',
            sa.Column('id_cliente', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('nombre', sa.String(), nullable=False),
            sa.Column('contacto', sa.String(), nullable=True),
            sa.Column('direccion', sa.String(), nullable=True),
            sa.Column('telefono', sa.String(), nullable=True),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
            sa.Column('alias', sa.String(), nullable=True),
            sa.Column('logo_url', sa.String(), nullable=True),
        )
    else:
        add_column_if_absent('cliente', sa.Column('alias', sa.String(), nullable=True))
        add_column_if_absent('cliente', sa.Column('logo_url', sa.String(), nullable=True))

    # PROYECTO
    if not has_table('proyecto'):
        op.create_table(
            'proyecto',
            sa.Column('id_proyecto', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_cliente', sa.Integer(), nullable=False),
            sa.Column('nombre', sa.String(), nullable=False),
            sa.Column('descripcion', sa.Text(), nullable=True),
            sa.Column('estado', sa.String(), nullable=True),
            sa.Column('fecha_inicio', sa.DateTime(), nullable=True),
            sa.Column('fecha_fin', sa.DateTime(), nullable=True),
            sa.Column('numero', sa.String(), nullable=True),
            sa.Column('id_integrador', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['id_cliente'], ['cliente.id_cliente']),
            sa.ForeignKeyConstraint(['id_integrador'], ['integrador.id_integrador']),
        )
    else:
        add_column_if_absent('proyecto', sa.Column('numero', sa.String(), nullable=True))
        add_column_if_absent('proyecto', sa.Column('id_integrador', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'proyecto', 'integrador', ['id_integrador'], ['id_integrador'])

    # TABLERO
    if not has_table('tablero'):
        op.create_table(
            'tablero',
            sa.Column('id_tablero', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_proyecto', sa.Integer(), nullable=False),
            sa.Column('codigo_tablero', sa.String(), nullable=False),
            sa.Column('descripcion', sa.Text(), nullable=True),
            sa.Column('id_tipo', sa.Integer(), nullable=True),
            sa.Column('ubicacion', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['id_proyecto'], ['proyecto.id_proyecto']),
            sa.ForeignKeyConstraint(['id_tipo'], ['tipo_tablero.id_tipo']),
        )
        add_unique_if_absent('uq_tablero_proyecto_codigo', 'tablero', ['id_proyecto', 'codigo_tablero'])
    else:
        add_column_if_absent('tablero', sa.Column('id_tipo', sa.Integer(), nullable=True))
        add_column_if_absent('tablero', sa.Column('ubicacion', sa.String(), nullable=True))
        # Intentamos dropear viejo tipo_tablero si existiera
        if has_column('tablero', 'tipo_tablero'):
            with op.batch_alter_table('tablero') as batch_op:
                try:
                    batch_op.drop_column('tipo_tablero')
                except Exception:
                    pass
        add_fk_if_absent(None, 'tablero', 'tipo_tablero', ['id_tipo'], ['id_tipo'])
        add_unique_if_absent('uq_tablero_proyecto_codigo', 'tablero', ['id_proyecto', 'codigo_tablero'])

    # INSPECCION
    if not has_table('inspeccion'):
        op.create_table(
            'inspeccion',
            sa.Column('id_inspeccion', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_proyecto', sa.Integer(), nullable=False),
            sa.Column('id_tablero', sa.Integer(), nullable=False),
            sa.Column('fecha_inspeccion', sa.DateTime(), nullable=True),
            sa.Column('inspector', sa.String(), nullable=True),
            sa.Column('conclusion_calidad', sa.String(), nullable=True),
            sa.Column('observaciones', sa.Text(), nullable=True),
            sa.Column('estado', sa.String(), nullable=True),
            sa.Column('tipo_visita', tipo_visita_enum, nullable=True),
            sa.Column('normativa', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['id_proyecto'], ['proyecto.id_proyecto']),
            sa.ForeignKeyConstraint(['id_tablero'], ['tablero.id_tablero']),
        )
    else:
        add_column_if_absent('inspeccion', sa.Column('tipo_visita', tipo_visita_enum, nullable=True))
        add_column_if_absent('inspeccion', sa.Column('normativa', sa.String(), nullable=True))
        add_column_if_absent('inspeccion', sa.Column('created_at', sa.DateTime(), nullable=True))
        add_column_if_absent('inspeccion', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # CHECKLIST (legacy) – si existe la dejamos, ya la “desacoplaste”; si no, no la creamos.

    # RESPUESTA_CHECKLIST
    if not has_table('respuesta_checklist'):
        op.create_table(
            'respuesta_checklist',
            sa.Column('id_respuesta', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_inspeccion', sa.Integer(), nullable=False),
            sa.Column('id_item', sa.Integer(), nullable=False),
            sa.Column('respuesta', sa.String(), nullable=True),
            sa.Column('observacion', sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(['id_inspeccion'], ['inspeccion.id_inspeccion']),
            sa.ForeignKeyConstraint(['id_item'], ['checklist_item.id_item']),
        )
        add_unique_if_absent('uq_respuesta_inspeccion_item', 'respuesta_checklist', ['id_inspeccion', 'id_item'])
    else:
        # Migración de columna si venía con id_checklist
        if has_column('respuesta_checklist', 'id_checklist'):
            with op.batch_alter_table('respuesta_checklist') as batch_op:
                try:
                    batch_op.drop_column('id_checklist')
                except Exception:
                    pass
        add_column_if_absent('respuesta_checklist', sa.Column('id_item', sa.Integer(), nullable=False))
        add_fk_if_absent(None, 'respuesta_checklist', 'checklist_item', ['id_item'], ['id_item'])
        add_unique_if_absent('uq_respuesta_inspeccion_item', 'respuesta_checklist', ['id_inspeccion', 'id_item'])

    # FOTO
    # FOTO
    if not has_table('foto'):
        op.create_table(
            'foto',
            sa.Column('id_foto', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_cliente', sa.Integer(), nullable=True),
            sa.Column('id_proyecto', sa.Integer(), nullable=True),
            sa.Column('id_tablero', sa.Integer(), nullable=True),
            sa.Column('id_inspeccion', sa.Integer(), nullable=True),
            sa.Column('id_item', sa.Integer(), nullable=True),
            sa.Column('id_informe', sa.Integer(), nullable=True),
            sa.Column('id_integrador', sa.Integer(), nullable=True),
            sa.Column('ruta_archivo', sa.String(), nullable=False),
            sa.Column('fecha_captura', sa.DateTime(), nullable=True),
            sa.Column('metadatos', sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(['id_cliente'], ['cliente.id_cliente']),
            sa.ForeignKeyConstraint(['id_proyecto'], ['proyecto.id_proyecto']),
            sa.ForeignKeyConstraint(['id_tablero'], ['tablero.id_tablero']),
            sa.ForeignKeyConstraint(['id_inspeccion'], ['inspeccion.id_inspeccion']),
            sa.ForeignKeyConstraint(['id_item'], ['checklist_item.id_item']),
            sa.ForeignKeyConstraint(['id_informe'], ['informe.id_informe']),
            sa.ForeignKeyConstraint(['id_integrador'], ['integrador.id_integrador']),
        )
        # Índice único para evitar duplicados
        add_unique_if_absent(
            'uq_foto_unica',
            'foto',
            ['id_cliente','id_proyecto','id_tablero','id_inspeccion','id_item','id_informe','id_integrador']
        )
    else:
        # Agregar nuevas columnas si faltan
        add_column_if_absent('foto', sa.Column('id_cliente', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'cliente', ['id_cliente'], ['id_cliente'])

        add_column_if_absent('foto', sa.Column('id_proyecto', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'proyecto', ['id_proyecto'], ['id_proyecto'])

        add_column_if_absent('foto', sa.Column('id_tablero', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'tablero', ['id_tablero'], ['id_tablero'])

        add_column_if_absent('foto', sa.Column('id_inspeccion', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'inspeccion', ['id_inspeccion'], ['id_inspeccion'])

        add_column_if_absent('foto', sa.Column('id_item', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'checklist_item', ['id_item'], ['id_item'])

        add_column_if_absent('foto', sa.Column('id_informe', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'informe', ['id_informe'], ['id_informe'])

        add_column_if_absent('foto', sa.Column('id_integrador', sa.Integer(), nullable=True))
        add_fk_if_absent(None, 'foto', 'integrador', ['id_integrador'], ['id_integrador'])

        # Crear índice único si no existe
        add_unique_if_absent(
            'uq_foto_unica',
            'foto',
            ['id_cliente','id_proyecto','id_tablero','id_inspeccion','id_item','id_informe','id_integrador']
        )

    # INFORME
    if not has_table('informe'):
        op.create_table(
            'informe',
            sa.Column('id_informe', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('id_proyecto', sa.Integer(), nullable=False),
            sa.Column('id_tablero', sa.Integer(), nullable=False),
            sa.Column('id_inspeccion', sa.Integer(), nullable=True),
            sa.Column('tipo_informe', sa.String(), nullable=True),
            sa.Column('nombre_archivo', sa.String(), nullable=True),
            sa.Column('ruta_archivo', sa.String(), nullable=True),
            sa.Column('fecha_generacion', sa.DateTime(), nullable=True),
            sa.Column('estado', sa.String(), nullable=True),
            sa.Column('numero_informe', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['id_proyecto'], ['proyecto.id_proyecto']),
            sa.ForeignKeyConstraint(['id_tablero'], ['tablero.id_tablero']),
            sa.ForeignKeyConstraint(['id_inspeccion'], ['inspeccion.id_inspeccion']),
        )
        add_unique_if_absent('uq_informe_inspeccion', 'informe', ['id_inspeccion'])
    else:
        add_column_if_absent('informe', sa.Column('id_inspeccion', sa.Integer(), nullable=True))
        add_column_if_absent('informe', sa.Column('numero_informe', sa.String(), nullable=True))
        add_fk_if_absent(None, 'informe', 'inspeccion', ['id_inspeccion'], ['id_inspeccion'])
        add_unique_if_absent('uq_informe_inspeccion', 'informe', ['id_inspeccion'])


def downgrade() -> None:
    # Downgrade cuidadoso (best-effort, puede ajustarse)
    # Quitar UNIQUE/FK en orden inverso
    try: op.drop_constraint('uq_informe_inspeccion', 'informe', type_='unique')
    except Exception: pass
    try: op.drop_constraint(None, 'informe', type_='foreignkey')
    except Exception: pass

    with op.batch_alter_table('informe') as batch_op:
        for col in ['id_inspeccion', 'numero_informe']:
            if has_column('informe', col):
                batch_op.drop_column(col)

    try: op.drop_constraint(None, 'foto', type_='foreignkey')
    except Exception: pass
    with op.batch_alter_table('foto') as batch_op:
        if has_column('foto', 'id_item'):
            batch_op.drop_column('id_item')

    try: op.drop_constraint('uq_respuesta_inspeccion_item', 'respuesta_checklist', type_='unique')
    except Exception: pass
    try: op.drop_constraint(None, 'respuesta_checklist', type_='foreignkey')
    except Exception: pass
    with op.batch_alter_table('respuesta_checklist') as batch_op:
        if has_column('respuesta_checklist', 'id_item'):
            batch_op.drop_column('id_item')
        # NO recreamos id_checklist (downgrade simplificado)

    try: op.drop_constraint('uq_tipo_plantilla', 'plantilla_por_tipo', type_='unique')
    except Exception: pass
    try: op.drop_table('plantilla_por_tipo')
    except Exception: pass
    try: op.drop_table('checklist_item')
    except Exception: pass
    try: op.drop_table('checklist_plantilla')
    except Exception: pass

    # Tablero
    try: op.drop_constraint('uq_tablero_proyecto_codigo', 'tablero', type_='unique')
    except Exception: pass
    try: op.drop_constraint(None, 'tablero', type_='foreignkey')
    except Exception: pass
    with op.batch_alter_table('tablero') as batch_op:
        for col in ['id_tipo','ubicacion']:
            if has_column('tablero', col):
                batch_op.drop_column(col)
        # (opcional) re-crear tipo_tablero texto

    # TipoTablero, Integrador (solo si se desea bajar completamente)
    try: op.drop_table('tipo_tablero')
    except Exception: pass
    try: op.drop_table('integrador')
    except Exception: pass

    # Cliente: quitar alias/logo si existen
    with op.batch_alter_table('cliente') as batch_op:
        for col in ['alias','logo_url']:
            if has_column('cliente', col):
                batch_op.drop_column(col)

    # Proyecto: quitar numero / id_integrador
    try: op.drop_constraint(None, 'proyecto', type_='foreignkey')
    except Exception: pass
    with op.batch_alter_table('proyecto') as batch_op:
        for col in ['numero','id_integrador']:
            if has_column('proyecto', col):
                batch_op.drop_column(col)

    # ENUM
    op.execute("DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_visita') THEN DROP TYPE tipo_visita; END IF; END $$;")
