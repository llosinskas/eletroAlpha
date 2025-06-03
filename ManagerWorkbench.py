import importlib
import FreeCADGui as Gui
import WorkbenchBase
import os

__title__ = WorkbenchBase.__title__

class AtualizarBancada:

    def Activated(self):
        Gui.removeWorkbench(__title__)
        # importlib.reload(__title__)
        print(__title__)

        importlib.reload(__title__)
        Gui.addWorkbench(__title__)
        # Gui.activateWorkbench("Circuits")

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'recompute.svg'), 'MenuText':'Inserir novo circuito elétrico', 'ToolTip':'Inserir um novo circuito elétrico elétrico'}



Gui.addCommand("AtualizarBancada",AtualizarBancada())
