import PySide
import os 
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui
import freecad.Circuits as WB

class GenerateReport:
    def GetResources(self):
        return {'Pixmap': os.path.join(WB.ICON_PATH, 'gerarPDF.svg'), 'MenuText':'Inserir novo circuito elétrico', 'ToolTip':'Inserir um novo circuito elétrico elétrico'}



Gui.addCommand("GenerateReport", GenerateReport())