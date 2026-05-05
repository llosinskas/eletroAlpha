import importlib
import FreeCADGui as Gui
import freecad.Circuits as WB
import os

__title__ = WB.__title__

class AtualizarBancada:

    def Activated(self):
        Gui.removeWorkbench(__title__)
        # importlib.reload(__title__)
        print(__title__)

        importlib.reload(__title__)
        Gui.addWorkbench(__title__)
        # Gui.activateWorkbench("Circuits")

    def GetResources(self):
        return {'Pixmap': os.path.join(WB.ICON_PATH, 'recompute.svg'), 'MenuText':'Inserir novo circuito elétrico', 'ToolTip':'Inserir um novo circuito elétrico elétrico'}



Gui.addCommand("AtualizarBancada",AtualizarBancada())

