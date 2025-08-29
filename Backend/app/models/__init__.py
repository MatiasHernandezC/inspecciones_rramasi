# Backend/app/models/__init__.py
from .base import Base  # aquí está tu declarative_base()

# importa todos los modelos para que Alembic los vea
from .cliente import Cliente
from .integrador import Integrador
from .proyecto import Proyecto
from .tipo_tablero import TipoTablero
from .tablero import Tablero
from .inspeccion import Inspeccion
from .checklist import Checklist
from .checklist_plantilla import ChecklistPlantilla
from .checklist_item import ChecklistItem
from .plantilla_por_tipo import PlantillaPorTipo
from .respuesta_checklist import RespuestaChecklist
from .foto import Foto
from .informe import Informe
