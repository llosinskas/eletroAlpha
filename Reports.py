import PySide
import os 
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui

class GenerateReport:
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'gerarPDF.svg'), 'MenuText':'Inserir novo circuito elétrico', 'ToolTip':'Inserir um novo circuito elétrico elétrico'}



Gui.addCommand("GenerateReport", GenerateReport())