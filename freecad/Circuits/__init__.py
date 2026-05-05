"""
Módulo de compatibilidade e constantes do workbench Circuits.
Substitui o antigo WorkbenchBase.py, fornecendo paths e metadados
para todos os comandos do workbench.
"""
import os
import sys

# Path base do pacote freecad.Circuits
__dir__ = os.path.dirname(os.path.abspath(__file__))

# Paths padronizados
ICON_PATH = os.path.join(__dir__, "Resources", "Icons")
IMAGE_PATH = os.path.join(__dir__, "Resources", "Images")
TABLE_PATH = os.path.join(__dir__, "Tables")
UI_PATH = os.path.join(__dir__, "UI")
LIBRARY_PATH = os.path.join(__dir__, "Componentes")
LOGGER_PATH = os.path.join(__dir__, "logs")

# Metadados
__title__ = "Engenharia"
__author__ = "Lucas Losinskas"
__url__ = "https://github.com/llosinskas/Circuits-FreeCAD"
__ToolTip__ = "Bancada para a criação e gerenciamento de projetos elétricos: Residênciais, Indústriais e Comerciais"

try:
    from .version import __version__
except ImportError:
    __version__ = "0.0.1"
