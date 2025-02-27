# Função para iniciar a bancada 
# Copyright Lucas Losinskas 
# year 2023

import os 
import FreeCADGui as Gui
import sys, FreeCAD
import WorkbenchBase



__title__ = WorkbenchBase.__title__
__author__ = WorkbenchBase.__author__
__url__ = WorkbenchBase.__url__

# paths configs
global logo_icon, path_base
path_base = WorkbenchBase.__dir__
logo_icon = os.path.join(WorkbenchBase.ICON_PATH, "logo.svg")


class Circuits(Workbench):
    
    MenuText = "Circuits"
    ToolTip = "Bancada para a criação de projetos elétricos: Residênciais, Indústriais e Comerciais"
    Icon = logo_icon

    def Initialize(self):
        """Essa função é executada quando a bancada é ativada pela primeira vez
        """

        import bimcommands
        # import BimWorkingPlaneTools
        import DraftTools
        import NewProject
        import EletricProject
        import InsertComponent
        import Arch
        import Draft
        # import BimWrappedTools
     
        
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
                "BIM_Sketch", 
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
       
        
        self.bimtools = [
            "BIM_Project",
            "Arch_Space", 
            "Arch_Wall", 
            "BIM_Column", 
            "BIM_Beam", 
            "BIM_Slab", 
            "BIM_Door", 
            "BIM_Library" 
            
        ]
        self.appendToolbar("BIM", self.bimtools)
        self.annotationtools = [
            "BIM_Text",
            "Arch_SectionPlane",
            "BIM_TDArchView",
            "BIM_Shape2DView",
        ]
        self.appendToolbar("Anotações", self.annotationtools)

        
        self.listProjects=[
            "ComponentEletric", 
            "Gerar3D", 
            "Cabo"
            ]
        self.appendToolbar("Alfa", self.listProjects)

        
        self.projectList=[
            'newProjetctEletrical',
            'newSpreadsheet', 
            'AddSpreadsheet', 
            'ListElements',
            'CreateModel'
            
            ]
        self.appendToolbar("Novo Projeto", self.projectList)

       
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


Gui.addWorkbench(Circuits())