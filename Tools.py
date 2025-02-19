import FreeCAD as App
import FreeCADGui as Gui
import Spreadsheet
import os

class GetSpaces():
    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("No active document found.\n")
            return 
        spaces = []
        for obj in doc.Objects:
        
            spaces.append(obj)
            print(obj)
            print(1)
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'newProject.svg'), 'MenuText': "Pegar Espaços", 'ToolTip':"Pegar todos os espaços do projeto"}
    
class ReiniciarBancada():
    def Activated(self):
        
        
        # InitGui.eletroAlpha(self).Initialize(self)
        Gui.activateWorkbench("eletroAlpha")
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'newProject.svg'), 'MenuText': "Novo Projeto", 'ToolTip':"Iniciar um novo projeto"}
    
Gui.addCommand("GetSpaces", GetSpaces())
Gui.addCommand("ReiniciarBancada", ReiniciarBancada())