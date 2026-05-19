"""
Módulo de compatibilidade para a bancada Circuits.
Redireciona as chamadas do antigo WorkbenchBase.py para o novo pacote freecad.Circuits.
"""
from freecad.Circuits import (
    ICON_PATH, IMAGE_PATH, TABLE_PATH, UI_PATH, LIBRARY_PATH, LOGGER_PATH,
    __title__, __author__, __url__, __ToolTip__, __version__
)
