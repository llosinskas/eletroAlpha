import PySide
import os 
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui
import WorkbenchBase




class ComponentEletric:
    def Activated(self):
        doc=App.activeDocument()
        # form_path = WorkbenchBase.UI_PATH
        # form = os.path.join(form_path, "WorkbenchBase.UI_PATH")

    def IsActive(self):
        return True
        
    def GetResources(self): 
        return {"Pixmap" :os.path.join(WorkbenchBase.ICON_PATH, 'Componentes.svg'),"MenuText": "Inserir um componente elétrico", "ToolTip":"Inserir um componente no projeto"}
    
class Gerar3D:  
    def GetResources(self):
        return {"Pixmap" : os.path.join(WorkbenchBase.ICON_PATH, "tomadas.svg"), "MenuText" : "Converter em 3D", "ToolTip":"Converter as informações inseridas em modelo 3D"}
    

Gui.addCommand("ComponentEletric", ComponentEletric())
Gui.addCommand("Gerar3D", Gerar3D())