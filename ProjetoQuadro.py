import os 
import FreeCAD as App
import FreeCADGui as Gui
import WorkbenchBase

class NewQuadro:
    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("No active document found.\n")
            return
        folder = doc.addObject("App::DocumentObjectGroup", "Dados")
        folder = doc.addObject("App::DocumentObjectGroup", "Estrutura funcional")
        folder = doc.addObject("App::DocumentObjectGroup", "Estrutura física")
        folder = doc.addObject("App::DocumentObjectGroup", "Documentacao")
        folder = doc.addObject("App::DocumentObjectGroup", "Dispositivos")
        folder = doc.addObject("App::DocumentObjectGroup", "Conexoes")
        folder = doc.addObject("App::DocumentObjectGroup", "Listagem")

        doc.recompute()

    def GetResources(self):
        return {'Pixmap': os.path.join(WorkbenchBase.ICON_PATH, 'newProject.svg'), 'MenuText': "Criar Quadro", 'ToolTip':"Criar um novo quadro elétrico"}
    
        
Gui.addCommand("NewQuadro", NewQuadro())