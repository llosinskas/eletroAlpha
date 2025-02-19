
# Função para iniciar a bancada 
# Copyright Lucas Losinskas 
# year 2023

import os 
import FreeCADGui
import Eletro_locator
import sys, FreeCAD

global logo_icon, eletro_path
eletro_path = os.path.dirname(Eletro_locator.__file__)
logo_icon = os.path.join(eletro_path, 'Resources/Icons/logo.svg')

class eletroAlpha(Workbench):
    MenuText = "Eletro Alpha"
    ToolTip = "Bancada para a criação de projetos elétricos: Residênciais, Indústriais e Comerciais"
    Icon = logo_icon

    def Initialize(self):
        """Essa função é executada quando a bancada é ativada pela primeira vez
        """
        
        import DraftTools
        self.snap = [
            "Draft_ToggleGrid", 
            "Draft_Snap_Lock", 
            "Draft_Snap_Midpoint", 
            "Draft_Snap_Perpendicular", 
            "Draft_Snap_Grid", 
            "Draft_Snap_Intersection", 
            "Draft_Snap_Parallel", 
            "Draft_Snap_Endpoint", 
            "Draft_Snap_Angle", 
            "Draft_Snap_Center", 
            "Draft_Snap_Extension", 
            "Draft_Snap_Near", 
            "Draft_Snap_Ortho", 
            "Draft_Snap_Special", 
            "Draft_Snap_Dimensions", 
            "Draft_Snap_WorkingPlane"
        ]
        self.appendToolbar("Snap", self.snap)
        
        self.draftingtools = [
                "Draft_Line",
                "Draft_Circle", 
                "Draft_Wire", 
                "Draft_Arc", 
                "Draft_Arc_3Points", 
                "Draft_Ellipse", 
                "Draft_Polygon", 
                "Draft_Rectangle", 
                "Draft_BSpline", 
                "Draft_BezCurve", 
                "Draft_Point", 
                 
        ]
        self.appendToolbar("desenho", self.draftingtools)
        
        self.modify = [
            "Draft_Move", 
            "Draft_Rotate", 
            "Draft_Offset", 
            "Draft_Trimex", 
            "Draft_Join", 
            "Draft_Scale", 
            "Draft_Edit", 
            "Draft_Mirror", 
            "Draft_OrthoArray", 
            "Draft_PathArray", 
        ]
        self.appendToolbar("Modificador", self.modify)
        import Arch
        self.bimtools = [
              "Arch_Space",
        ]
        self.appendToolbar("BIM", self.bimtools)
    

        import NewProject
        self.projectList=['newProjetctEletrical', 'newSpreadsheet']
        self.appendToolbar("Novo Projeto", self.projectList)

        import InsertComponent
        self.componenents=['InsertComponent', 'InsertTugs', 'InsertEquipaments', 'InsertWire', 'InsertConduit', 'InsertCableTray']
        self.appendToolbar('Inserir Componentes', self.componenents)

        import Reports
        self.listreports = ['GenerateReport']
        self.appendToolbar('Gerar o relatório da instalação', self.listreports)

        import Tools
        self.listTools = ["GetSpaces", "ReiniciarBancada"]
        self.appendToolbar("Ferramentas", self.listTools)

        FreeCADGui.updateGui()
    def Activated(self):
        return 
    
    def Deactivated(self): 
        return 
    
    def ContextMenu(self, recipient):
        self.appendContextMenu("EletroAlfa", self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(eletroAlpha())