# Iniatilize some paths
import os 
import sys

# Path 
try: 
    __dir__ = os.path.dirname(sys.modules[__name__].__file__)
except(AttributeError, KeyError):
    __dir__ = os.path.dirname(os.path.abspath(sys.arg[0]))
ICON_PATH = os.path.join(__dir__, "Resources","Icons")
IMAGE_PATH = os.path.join(__dir__, "Resource","Images")
TABLE_PATH = os.path.join(__dir__, "Tables")
UI_PATH = os.path.join(__dir__, "UI")
PROJECT_BIM = os.path.join(__dir__, "core","projectsbim")
LIBRARY_PATH = os.path.join(__dir__, "Componentes")
LOGGER_PATH = os.path.join(__dir__, "logs")

# Name 
__title__ = "Engenharia"
__author__ = "Lucas Losinskas"
__url__ = "https://github.com/llosinskas/eletroAlpha"
__ToolTip__ = "Bancada para a criação e gerenciamento de projetos elétricos: Residênciais, Indústriais e Comerciais"
__version__ = "0.01"