
import FreeCAD as App
import FreeCADGui as Gui
import os
import sys 
import importlib


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
        try:
            import WorkbenchBase
            workbench_name = WorkbenchBase.__title__
            
            # Lista de módulos para remover e recarregar
            modules_to_reload = [
                'NewProject',
                'EletricProject',
                'InsertComponent',
                'Tools',
                'GerarUnifilar',
                'Reports',
                'importQEletrotech',
                'ManagerWorkbench',
                'Eletro_libs',
                'calculo_cabo',
                'UI.dialogs',
                'UI.dialogs.ComponentSelectorDialog',
                'UI.dialogs.ComponentInserter',
            ]
            
            # Remove módulos do sys.modules
            for module_name in list(sys.modules.keys()):
                if any(module_name == mod or module_name.startswith(mod + '.') for mod in modules_to_reload):
                    del sys.modules[module_name]
            
            # Recarrega WorkbenchBase
            importlib.reload(WorkbenchBase)
            
            # Remove InitGui para forçar reimportação limpa
            if 'InitGui' in sys.modules:
                del sys.modules['InitGui']
            
            import InitGui
            
            # Ativa a bancada novamente
            Gui.activateWorkbench(workbench_name)
            Gui.updateGui()
            
            App.Console.PrintMessage("✓ Bancada recarregada com sucesso!\n")
            
        except Exception as e:
            App.Console.PrintError(f"Erro ao recarregar bancada: {str(e)}\n")

    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'recompute.svg'), 
            'MenuText': "Reiniciar Bancada", 
            'ToolTip': "Recarregar todos os módulos da bancada sem fechar o FreeCAD"
        }
    
Gui.addCommand("GetSpaces", GetSpaces())
Gui.addCommand("ReiniciarBancada", ReiniciarBancada())