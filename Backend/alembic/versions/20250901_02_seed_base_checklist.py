"""Seed base checklist plantilla and items (idempotent)

Revision ID: 20250901_02_seed_base_checklist
Revises: 20250901_01_dbml_alignment
Create Date: 2025-09-01 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20250901_02_seed_base_checklist"
down_revision = "20250901_01_dbml_alignment"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    meta = sa.MetaData()

    checklist_plantilla = sa.Table(
        "checklist_plantilla",
        meta,
        sa.Column("id_plantilla", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String),
        sa.Column("descripcion", sa.Text),
        sa.Column("version", sa.Integer),
        sa.Column("vigente", sa.Boolean),
    )
    checklist_item = sa.Table(
        "checklist_item",
        meta,
        sa.Column("id_item", sa.Integer, primary_key=True),
        sa.Column("id_plantilla", sa.Integer),
        sa.Column("seccion", sa.String),
        sa.Column("nombre_item", sa.String),
        sa.Column("tipo_item", sa.String),
        sa.Column("required", sa.Boolean),
        sa.Column("orden", sa.Integer),
        sa.Column("reglas", sa.Text),
    )
    tipo_tablero = sa.Table(
        "tipo_tablero",
        meta,
        sa.Column("id_tipo", sa.Integer, primary_key=True),
    )
    plantilla_por_tipo = sa.Table(
        "plantilla_por_tipo",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("id_tipo", sa.Integer),
        sa.Column("id_plantilla", sa.Integer),
    )

    # 0) Limpieza idempotente de plantillas previas con mismo nombre
    #    Evita duplicados de ejecuciones anteriores
    for nombre_cleanup in ["Base Informe Calidad", "Base Informe Calidad Lite"]:
        res_ids = bind.execute(
            sa.text(
                "SELECT id_plantilla FROM checklist_plantilla WHERE nombre = :n"
            ),
            {"n": nombre_cleanup},
        ).fetchall()
        ids = [r[0] for r in res_ids]
        if ids:
            bind.execute(
                sa.text(
                    "DELETE FROM plantilla_por_tipo WHERE id_plantilla = ANY(:ids)"
                ),
                {"ids": ids},
            )
            bind.execute(
                sa.text(
                    "DELETE FROM checklist_item WHERE id_plantilla = ANY(:ids)"
                ),
                {"ids": ids},
            )
            bind.execute(
                sa.text(
                    "DELETE FROM checklist_plantilla WHERE id_plantilla = ANY(:ids)"
                ),
                {"ids": ids},
            )

    # 1) Upsert plantilla base
    nombre = "Base Informe Calidad"
    descripcion = "Plantilla base para informes de inspección visual y pruebas."
    version = 1
    vigente = True

    existing = bind.execute(
        sa.select(checklist_plantilla.c.id_plantilla).where(
            checklist_plantilla.c.nombre == nombre,
            checklist_plantilla.c.version == version,
        )
    ).fetchone()

    if existing:
        plantilla_id = existing[0]
    else:
        res = bind.execute(
            checklist_plantilla.insert().values(
                nombre=nombre, descripcion=descripcion, version=version, vigente=vigente
            )
        )
        # for Postgres, res.inserted_primary_key may be None in Alembic context; fetch again
        row = bind.execute(
            sa.select(checklist_plantilla.c.id_plantilla).where(
                checklist_plantilla.c.nombre == nombre,
                checklist_plantilla.c.version == version,
            )
        ).fetchone()
        plantilla_id = row[0]

    # 2) Items: boolean tri-estado (P/F/N) con observación libre
    # Secciones y entradas (orden numérico conserva estructura del informe)
    def b(sec, text, orden):
        return dict(seccion=sec, nombre_item=text, tipo_item="boolean", required=True, orden=orden, reglas=None)

    items = []

    # 1.0 INSPECCIÓN VISUAL / PRESENTACIÓN
    sec = "INSPECCIÓN VISUAL"
    items += [
        b(sec, "1.1 LIMPIEZA INTERNA Y EXTERNA", 101),
        b(sec, "1.3 CABLEADO ORDENADO Y AMARRADO", 103),
        b(sec, "1.4 CORTES LIMADOS Y PINTADO (BARRAS, RIELES, PERFORACIONES, ETC.)", 104),
        b(sec, "1.5 EMBALAJE APROPIADO PARA REVISION Y TRANSPORTE (Identificación)", 105),
    ]

    # 2.0 DOCUMENTACION
    sec = "DOCUMENTACIÓN"
    items += [
        b(sec, "2.1 CARPETA con documentación fichas técnicas, planos y listados", 201),
        b(sec, "2.2 INFORMACION ADHERIDA: Cuadro cargas y unilineal asbuilt", 202),
        b(sec, "2.3 CHECKLIST DE INTEGRADOR", 203),
    ]

    # 3.0 TABLERO
    sec = "TABLERO"
    items += [
        b(sec, "3.1 CERTIFICADO FABRICANTE DE LA ENVOLVENTE", 301),
        b(sec, "3.2 VERIFICACION DE TIPO DE COMPARTIMENTACION REQUERIDA", 302),
        b(sec, "3.3 VERIFICACION DE IK REQUERIDO", 303),
        b(sec, "3.4 IP REQUERIDO MÍNIMOS: 41 INT., 44 EXT. BAJO TECHO, 54 AGUA", 304),
        b(sec, "3.5 MODELO DE TABLERO SEGÚN LO REQUERIDO (IP Y DIMENSIONES)", 305),
        b(sec, "3.6 PUERTAS (chapa, llaves, cierre/apertura, puesta a tierra)", 306),
        b(sec, "3.7 ZOCALOS (Frontales, laterales, posteriores, pernos)", 307),
        b(sec, "3.8 CANCAMOS DE IZAJE", 308),
        b(sec, "3.9 SELLO ENTRE CUERPOS DEL TABLERO", 309),
        b(sec, "3.10 MATERIALES NO PROPAGADORES DE LLAMA", 310),
        b(sec, "3.11 25% CRECIMIENTO PARA C/TIPO DE SERVICIO QUE CONTENGA EL TABLERO", 311),
        b(sec, "3.12 VERIFICACION VENTILACION SEGÚN ESPECIFICACION", 312),
        b(sec, "3.13 ALTURA MIN Y MAX DISPOSITIVOS 0.45-2.0 m", 313),
        b(sec, "3.14 PROTECCION BARRAS DISTRIBUCION Y SENALIZACION RIESGO", 314),
        b(sec, "3.15 >100A => INSTRUMENTOS DE MEDICION CORRIENTE Y TENSION POR FASE", 315),
        b(sec, "3.16 LUCES PILOTO CONECTADA DESDE ENTRADA ALIMENTADOR", 316),
        b(sec, "3.17 TABLERO GENERAL/DISTRIBUCION (>3 ctos) => CORTE 4P", 317),
        b(sec, "3.18 DISTINTOS SERVICIOS EN SECCIONES DISTINTAS", 318),
        b(sec, "3.19 DISTINTOS SERVICIOS CON ITM GENERAL DE CORTE 4P (>3 ctos)", 319),
        b(sec, "3.20 TABLERO FAENA MOVIL CON PARADA EMERGENCIA EXTERIOR", 320),
        b(sec, "3.21 TABLERO FAENA MOVIL IP MÍNIMO 56", 321),
        b(sec, "3.22 TABLERO FAENA MOVIL IK MÍNIMO 07", 322),
        b(sec, "3.23 TABLERO PROVISIONAL: TODOS LOS CIRCUITOS CON DIFERENCIAL", 323),
        b(sec, "3.24 TABLERO PROVISIONAL CTO. <= 32A => DIFERENCIAL <=30mA", 324),
        b(sec, "3.25 TABLERO PROVISIONAL CTO. > 32A => DIFERENCIAL <=300mA", 325),
        b(sec, "3.26 GESTION TERMICA: CAUDAL SEGÚN DISEÑO", 326),
        b(sec, "3.27 ESPACIO 25% DE CRECIMIENTO EN BARRAS", 327),
        b(sec, "3.28 CONFORMIDAD EQUIPOS ESPECIFICADOS (EETT, LISTA MATERIALES)", 328),
    ]

    # 4.0 SEÑALÉTICA E IDENTIFICACIÓN
    sec = "SEÑALÉTICA E IDENTIFICACIÓN"
    items += [
        b(sec, "4.1 PLACA INTERIOR IDENTIFICACIÓN PRODUCTO", 401),
        b(sec, "4.2 PLACA EXTERIOR LEGRAND", 402),
        b(sec, "4.3 ETIQUETA DE SERIE", 403),
        b(sec, "4.4 ETIQUETAS DE PELIGRO POR TENSION", 404),
    ]

    # 5.0 REGLETAS / REPARTIDORES / BARRAS
    sec = "REGLETAS / REPARTIDORES / BARRAS"
    items += [
        b(sec, "5.1 DIMENSIONES BARRAS FASE/NEUTRO/TIERRA; MATERIAL Y TRATAMIENTO", 501),
        b(sec, "5.2 CAPACIDAD CORTOCIRCUITO POR N° DE SOPORTES", 502),
        b(sec, "5.3 TORQUES DE APRIETE", 503),
        b(sec, "5.4 DISTANCIAS DE AISLAMIENTO (Uimp)", 504),
        b(sec, "5.5 COBERTURA AISLANTE INSTALADA (Fases+N+T)", 505),
        b(sec, "5.6 CÓDIGO DE COLORES E IDENTIFICACION (Fases+N+T)", 506),
        b(sec, "5.7 OTRAS BARRAS (TCOMP, ETC.)", 507),
        b(sec, "5.8 PERFORACIONES EN BARRAS SEGÚN CAPACIDAD", 508),
        b(sec, "5.9 25% CRECIMIENTO EN BARRAS DE DISTRIBUCIÓN", 509),
        b(sec, "5.10 SECUENCIA AZUL-NEGRO-ROJO, R-S-T 6.2.9", 510),
        b(sec, "5.11 ESPACIO 25% DE CRECIMIENTO CADA SERVICIO", 511),
    ]

    # 6.0 PROTECCIONES/DIFERENCIALES/CONTACTOR/VENTILADOR
    sec = "PROTECCIONES / DIFERENCIALES / CONTACTOR / VENTILADOR"
    items += [
        b(sec, "6.1 CONFORMIDAD SEGÚN PLANOS UNILINEAL Y DISPOSICIÓN", 601),
        b(sec, "6.2 CORRIENTE NOMINAL POR CADA INTERRUPTOR", 602),
        b(sec, "6.3 CORRIENTE CORTOCIRCUITO SEGÚN PLANO", 603),
        b(sec, "6.4 PROTECCIÓN REGULADA SEGÚN PLANO", 604),
        b(sec, "6.5 FUNCIONAMIENTO MECÁNICO DE PROTECCIONES", 605),
        b(sec, "6.6 BOBINA DE CIERRE Y APERTURA (Tensión Nominal)", 606),
        b(sec, "6.7 TIPO DE DIFERENCIAL SEGÚN PLANOS (AC, HPI, ETC.)", 607),
        b(sec, "6.8 CORRIENTE DE SENSIBILIDAD DIFERENCIAL", 608),
        b(sec, "6.9 CANTIDAD DE POLOS", 609),
        b(sec, "6.10 TENSIÓN DE SERVICIO", 610),
        b(sec, "6.11 IDENTIFICACION DE LA PROTECCION", 611),
        b(sec, "6.12 TOPES DE FIJACIÓN A AMBOS LADOS", 612),
        b(sec, "6.13 PANTALLAS CORTA-CHISPAS", 613),
        b(sec, "6.14 BOBINA DE CONTACTORES Y RELES (Tensión Nominal)", 614),
        b(sec, "6.15 TORQUES DE APRIETE (PROTOCOLO TSE)", 615),
        b(sec, "6.16 RAZÓN T/C SEGÚN UNILINEAL Y ESCALA AMPERÍMETRO", 616),
    ]

    # 7.0 BORNES
    sec = "BORNES"
    items += [
        b(sec, "7.1 CALIBRE VS SECCIÓN CONDUCTORES", 701),
        b(sec, "7.2 ESPACIO 25% DE CRECIMIENTO CADA SERVICIO", 702),
        b(sec, "7.3 IDENTIFICACION Y MARCAS", 703),
        b(sec, "7.4 TAPA FINAL", 704),
        b(sec, "7.5 TOPES DE FIJACIÓN", 705),
        b(sec, "7.6 TIERRA COMPUTACIÓN SEPARADA DE TP", 706),
        b(sec, "7.7 ACCESO LIBRE PARA CONDUCTORES", 707),
        b(sec, "7.8 TORQUES DE APRIETE: TERMINALES Y ACCESORIOS (PROTOCOLO TSE)", 708),
        b(sec, "7.9 BARRAS ENTRADA/SALIDA PARA CONDUCTORES EXTERNOS", 709),
    ]

    # 8.0 CANALIZACION
    sec = "CANALIZACION"
    items += [
        b(sec, "8.1 ACCESO DISYUNTOR GENERAL", 801),
        b(sec, "8.2 ACCESO LIBRE PARA MANTENIMIENTO", 802),
        b(sec, "8.3 RETARDANTE A LA LLAMA Y AUTOEXTINGUIBLE", 803),
        b(sec, "8.4 BANDEJA PORTACONDUCTORES OCUPA <=50% SECCION", 804),
    ]

    # 9.0 CONDUCTORES DE POTENCIA Y CONTROL
    sec = "CONDUCTORES DE POTENCIA Y CONTROL"
    items += [
        b(sec, "9.1 COLORES: F1 AZUL, F2 NEGRO, F3 ROJO, N BLANCO, T VERDE/AMARILLO", 901),
        b(sec, "9.2 SECCIONES VS CORRIENTE NOMINAL", 902),
        b(sec, "9.3 AISLACIÓN LIBRE DE HALÓGENOS", 903),
        b(sec, "9.4 SECCIÓN CONDUCTORES DE CONTROL", 904),
        b(sec, "9.5 AISLACIÓN CONDUCTORES DE CONTROL", 905),
        b(sec, "9.6 ESTADO DE AISLACIÓN", 906),
        b(sec, "9.7 RADIO DE CURVATURA VS CALIBRE", 907),
        b(sec, "9.8 CALIBRE TERMINALES VS SECCIÓN", 908),
        b(sec, "9.9 AISLACIÓN DE TERMINALES", 909),
        b(sec, "9.10 FIJACIONES Y SOPORTES", 910),
        b(sec, "9.11 TORQUES DE APRIETE (PROTOCOLO TSE)", 911),
        b(sec, "9.12 IDENTIFICACIÓN CIRCUITOS CON MARCAS", 912),
    ]

    # 10.0 ASPECTO ELÉCTRICO
    sec = "ASPECTO ELÉCTRICO"
    items += [
        b(sec, "10.1 CABLEADO RESPECTO A DIAGRAMA UNILINEAL", 1001),
        b(sec, "10.2 IDENTIFICACIÓN CIRCUITOS MEDIANTE MARCAS", 1002),
        b(sec, "10.3 PRESENCIA DE FUSIBLES EN PORTAFUSIBLES", 1003),
        b(sec, "10.4 CORRIENTE NOMINAL FUSIBLES SEGÚN PLANOS", 1004),
        b(sec, "10.5 DISTRIBUCIÓN DE FASES VS CUADRO DE CARGAS", 1005),
    ]

    # 11.0 CONTINUIDAD DE CIRCUITOS
    sec = "CONTINUIDAD DE CIRCUITOS"
    items += [
        b(sec, "11.1 CONTINUIDAD HASTA ÚLTIMO PUNTO (por circuito)", 1101),
        b(sec, "11.2 PARTES METÁLICAS A TIERRA (Nota 3)", 1102),
    ]

    # 12.0 PRUEBAS DE AISLACIÓN (400V-230V)
    sec = "PRUEBAS DE AISLACIÓN (400V-230V) - Nota 1"
    items += [
        b(sec, "12.1 AISLACIÓN ENTRE FASES", 1201),
        b(sec, "12.2 AISLACIÓN ENTRE FASE 1 Y NEUTRO", 1202),
        b(sec, "12.3 AISLACIÓN ENTRE FASE 2 Y NEUTRO", 1203),
        b(sec, "12.4 AISLACIÓN ENTRE FASE 3 Y NEUTRO", 1204),
        b(sec, "12.5 AISLACIÓN ENTRE FASE 1 Y TIERRA", 1205),
        b(sec, "12.6 AISLACIÓN ENTRE FASE 2 Y TIERRA", 1206),
        b(sec, "12.7 AISLACIÓN ENTRE FASE 3 Y TIERRA", 1207),
        b(sec, "12.8 AISLACIÓN ENTRE NEUTRO Y TIERRA", 1208),
        b(sec, "12.9 VERIFICACION CON TESTER DE CONTINUIDAD", 1209),
        b(sec, "12.10 TENSIÓN SOPORTADA A FRECUENCIA INDUSTRIAL (Nota 2)", 1210),
    ]

    # 13.0 PRUEBAS DE FUNCIONAMIENTO CON TENSIÓN DE OPERACIÓN
    sec = "PRUEBAS DE FUNCIONAMIENTO CON TENSIÓN DE OPERACIÓN"
    items += [
        b(sec, "13.1 LUCES PILOTO: NORMAL Y EMERGENCIA", 1301),
        b(sec, "13.2 TENSIÓN EN BORNES DE SALIDA (por circuito)", 1302),
        b(sec, "13.3 NIVEL DE TENSIÓN RESPECTO A MASA", 1303),
        b(sec, "13.4 SISTEMA DE CONTROL (COMANDO)", 1304),
        b(sec, "13.5 PROTECCIONES ENTREGADAS EN POSICIÓN OFF", 1305),
    ]

    # 14.0 APARATOS DE MEDIDA
    sec = "APARATOS DE MEDIDA"
    items += [
        b(sec, "14.1 VISUALIZACIÓN DE VARIABLES Y TENSIÓN DE LLEGADA", 1401),
        b(sec, "14.2 VOLTAJES PRIM. Y SEC. DEL TRANSF. DE CONTROL", 1402),
    ]

    # 15.0 CORRECTOR FACTOR DE POTENCIA
    sec = "CORRECTOR FACTOR DE POTENCIA"
    items += [
        b(sec, "15.1 RAZÓN DE TRANSFORMACIÓN EN CONTROLADOR", 1501),
        b(sec, "15.2 PASOS PROGRAMADOS", 1502),
        b(sec, "15.3 ENTRADA PASOS MANUAL", 1503),
        b(sec, "15.4 VENTILADOR Y TERMOSTATO", 1504),
    ]

    # 16.0 TRANSFERENCIA ATS
    sec = "TRANSFERENCIA ATS"
    items += [
        b(sec, "16.1 FUNCIONAMIENTO DE LOS DISTINTOS MENÚS", 1601),
        b(sec, "16.2 CORTE DE ENERGÍA: CB NO CAMBIAN DE ESTADO", 1602),
        b(sec, "16.3 CONTACTOS AUX DE CB CABLEADOS A ATS", 1603),
    ]

    # 17.0 FUENTE DE PODER
    sec = "FUENTE DE PODER"
    items += [
        b(sec, "17.1 TENSIÓN DE ALIMENTACIÓN Y SALIDA", 1701),
        b(sec, "17.2 ELEMENTOS DE PROTECCIÓN (INTERRUPTOR, FUSIBLES)", 1702),
    ]

    # 18.0 TRANSFORMADOR DE CONTROL
    sec = "TRANSFORMADOR DE CONTROL"
    items += [
        b(sec, "18.1 TENSIÓN PRIMARIO/SECUNDARIO SEGÚN PLACA", 1801),
        b(sec, "18.2 ELEMENTOS DE PROTECCIÓN (INT., PORTAFUSIBLES, FUSIBLES)", 1802),
    ]

    # 19.0 CONTACTORES Y RELES
    sec = "CONTACTORES Y RELES"
    items += [
        b(sec, "19.1 FUNCIONAMIENTO SEGÚN LÓGICA DE CONTROL", 1901),
        b(sec, "19.2 PULSADORES Y SELECTORES", 1902),
        b(sec, "19.3 PILOTOS DE SEÑALIZACIÓN", 1903),
    ]

    # 20.0 PROTECCIONES DIFERENCIALES
    sec = "PROTECCIONES DIFERENCIALES"
    items += [
        b(sec, "20.1 PRUEBA DE FUNCIONAMIENTO SEGÚN IEC 61557-6", 2001),
    ]

    # Insert items (limpio por nombre)
    for it in items:
        bind.execute(
            checklist_item.insert().values(
                id_plantilla=plantilla_id,
                seccion=it["seccion"],
                nombre_item=it["nombre_item"],
                tipo_item=it["tipo_item"],
                required=it["required"],
                orden=it["orden"],
                reglas=it["reglas"],
            )
        )

    # 3) Tipos de tablero requeridos (insert if not exists)
    tipos_requeridos = [
        "Autosoportado",
        "Residencial",
        "Murales",
        "Combinados",
        "Banco Condensadores Murales",
        "Banco Condensadores Autosoportados",
    ]
    tipo_tab_rows = dict(
        bind.execute(sa.text("SELECT nombre, id_tipo FROM tipo_tablero")).fetchall()
    )
    ids_tipos = {}
    for nombre_tipo in tipos_requeridos:
        if nombre_tipo in tipo_tab_rows:
            ids_tipos[nombre_tipo] = tipo_tab_rows[nombre_tipo]
        else:
            res = bind.execute(
                sa.text(
                    "INSERT INTO tipo_tablero (nombre, categoria, activo) VALUES (:n, NULL, TRUE) RETURNING id_tipo"
                ),
                {"n": nombre_tipo},
            )
            ids_tipos[nombre_tipo] = res.scalar()

    # 4) Crear plantilla LITE (solo primer item por seccion)
    lite_nombre = "Base Informe Calidad Lite"
    lite_existing = bind.execute(
        sa.select(checklist_plantilla.c.id_plantilla).where(
            checklist_plantilla.c.nombre == lite_nombre,
            checklist_plantilla.c.version == version,
        )
    ).fetchone()
    if lite_existing:
        lite_id = lite_existing[0]
    else:
        bind.execute(
            checklist_plantilla.insert().values(
                nombre=lite_nombre,
                descripcion="Plantilla base reducida (primer item por sección)",
                version=version,
                vigente=True,
            )
        )
        lite_id = bind.execute(
            sa.select(checklist_plantilla.c.id_plantilla).where(
                checklist_plantilla.c.nombre == lite_nombre,
                checklist_plantilla.c.version == version,
            )
        ).scalar()

    # Determinar primer item por sección según 'orden'
    from collections import defaultdict

    first_by_sec = {}
    for it in items:
        sec = it["seccion"]
        if sec not in first_by_sec or it["orden"] < first_by_sec[sec]["orden"]:
            first_by_sec[sec] = it

    # Insertar items lite
    for it in first_by_sec.values():
        bind.execute(
            checklist_item.insert().values(
                id_plantilla=lite_id,
                seccion=it["seccion"],
                nombre_item=it["nombre_item"],
                tipo_item=it["tipo_item"],
                required=it["required"],
                orden=it["orden"],
                reglas=it["reglas"],
            )
        )

    # 5) Vincular por tipo: Autosoportado -> full; otros -> lite
    for nombre_tipo, id_tipo in ids_tipos.items():
        objetivo = plantilla_id if nombre_tipo == "Autosoportado" else lite_id
        link_exists = bind.execute(
            sa.select(sa.func.count())
            .select_from(plantilla_por_tipo)
            .where(
                plantilla_por_tipo.c.id_tipo == id_tipo,
                plantilla_por_tipo.c.id_plantilla == objetivo,
            )
        ).scalar()
        if not link_exists:
            bind.execute(
                plantilla_por_tipo.insert().values(
                    id_tipo=id_tipo, id_plantilla=objetivo
                )
            )


def downgrade() -> None:
    # No borramos la plantilla ni items para evitar pérdida de datos; noop
    pass
