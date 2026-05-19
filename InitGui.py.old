"""
Módulo para iniciar a bancada de projetos elétricos, onde serão listados os comandos para criar um novo projeto, gerar o diagrama unifilar, criar a planilha de circuitos, entre outros.

Author: Lucas Losinskas
Date: 2026
Última atualização: 2026-03
Versão: 0.01
"""

import os 
import sys
import FreeCADGui as Gui
from FreeCADGui import Workbench
import FreeCAD
import WorkbenchBase


class Circuits(Workbench):
    """Bancada para a criação e gerenciamento de projetos elétricos.
    Interface para criar novos projetos, modificação, componentes elétricos, geração de diagramas unifilares, entre outros.

    Attributes:
        __title__(str): Título da bancada
        MenuText(str): Texto exibido no menu
        ToolTip(str): Dica exibida ao deixar o mouse sobre o comando
        Icon(str): Caminho para o ícone da bancada
    """
    # Tem que importar dentro da classe para evitar erros de importação circular, já que os comandos importam a bancada e a bancada importa os comandos.
    import WorkbenchBase
    WORKBENCH_NAME = WorkbenchBase.__title__
    TOOLTIP = WorkbenchBase.__ToolTip__
    LOGO_ICON = os.path.join(WorkbenchBase.ICON_PATH, "logo.svg")

    MenuText = WORKBENCH_NAME
    ToolTip = TOOLTIP
    Icon = LOGO_ICON

    # ==========================================
    # Definição de toolbar
    SNAP_TOOLS = [
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
    DRAWING_TOOLS = [
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
    MODIFY_TOOLS = [
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
        "Draft_Draft2Sketch",
    ]
    BIM_TOOLS = [
        "BIM_Project",
        "Arch_Space", 
        "Arch_Wall", 
        "BIM_Column", 
        "BIM_Beam", 
        "BIM_Slab", 
        "BIM_Door", 
        "BIM_Library" 
    ]
    
    ANNOTATION_TOOLS = [
        "BIM_Text",
        "Arch_SectionPlane",
        "BIM_TDView",
        "BIM_Shape2DView",
    ]
    
    PROJECT_TOOLS = [
        "ComponentEletric", 
        "Gerar3D", 
        "Cabo"
    ]
    NEW_PROJECT_TOOLS = [
        'newProjetctEletrical',
        'newSpreadsheet', 
        'AddSpreadsheet', 
        'ListElements',
        'CreateModel'
    ]
    
    INSERT_COMPONENTS_TOOLS = [
        'InsertComponent', 
        'InsertTugs', 
        'InsertEquipaments', 
        'InsertWire', 
        'InsertConduit', 
        'InsertCableTray'
    ]
    REPORT_TOOLS = [
        'GenerateReport'
    ]
    
    UTILITY_TOOLS = [
        "GetSpaces", 
        "ReiniciarBancada"
    ]
    
    UNIFILAR_TOOLS = [
        "GerarUnifilar", 
        "GerarPlanilha", 
        "AddCircuito"
    ]
    
    QELETROTECH_TOOLS = [
        "ImportQET",
        "Add_Node"
    ]
    
    QUADRO_TOOLS = [
        "NewQuadro"
    ]

    # ==========================================
    # Definição de toolbars com labels 
    TOOLBARS = [
        ("Snap", SNAP_TOOLS),
        ("Desenho", DRAWING_TOOLS),
        ("Modificador", MODIFY_TOOLS),
        ("BIM", BIM_TOOLS),
        ("Anotações", ANNOTATION_TOOLS),
        ("Inserir Componentes", PROJECT_TOOLS),
        ("Novo Projeto", NEW_PROJECT_TOOLS),
        ("Componentes", INSERT_COMPONENTS_TOOLS),
        ("Relatórios", REPORT_TOOLS),
        ("Ferramentas", UTILITY_TOOLS),
        ("Diagrama Unifilar", UNIFILAR_TOOLS),
        ("QEletrotech", QELETROTECH_TOOLS),
        ("Quadro Elétrico", QUADRO_TOOLS),
    ]    

    def _import_required_modules(self)->None:
        """Importa todos os módulos necessários para a bancadada
        Agrupa todos as importações para organizar melhor o código 
        """
        import bimcommands
        import DraftTools
        import NewProject
        import EletricProject
        import InsertComponent
        import Arch
        import Draft
        import GerarUnifilar
        import Reports
        import Tools
        import importQEletrotech
        import ProjetoQuadro
    def _setup_toolbars(self) ->None:
        """ Configura todas as toolbars da bancadas. 
        Itera sobre as Toolbars e adiciona cada uma delas

        Returns: 
            None
        """
        for label, tools in self.TOOLBARS:
            self.appendToolbar(label, tools)

    def _setup_menus(self) -> None:
        """Configura os menus da bancada.
        
        Returns:
            None
        """
        # Menu Componentes
        self.appendMenu("&Componentes", self.INSERT_COMPONENTS_TOOLS)
        
        # Menu Novo Projeto
        self.appendMenu("&Novo Projeto", self.NEW_PROJECT_TOOLS)
        
        # Menu Diagrama Unifilar
        self.appendMenu("&Diagrama Unifilar", self.UNIFILAR_TOOLS)
        
        # Menu Quadro Elétrico
        self.appendMenu("&Quadro Elétrico", self.QUADRO_TOOLS)
        
        # Menu Relatórios
        self.appendMenu("&Relatórios", self.REPORT_TOOLS)

    def Initialize(self)->None:
        """Essa função é executada quando a bancada é ativada pela primeira vez
        Returns:
            None
        """
        self._import_required_modules()
        self._setup_toolbars()
        self._setup_menus()
        Gui.updateGui()


    def Activated(self):
        """Executado quando a bancada é ativada
        
        Returns:
            None
        """
        # Inicializa ícones com suporte a tema dark
        try:
            from utils.icon_manager import initialize_dark_theme_icons
            initialize_dark_theme_icons()
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar ícones otimizados: {e}")
        
        print("✓ Bancada Eletro Alpha ativada!")
        print("  → Sistema de Componentes pronto")
        print("  → Toolbar 'Componentes' disponível")
        print("  → Menu 'Componentes' disponível")
        return 
    
    def Deactivated(self): 
        """Executado quando a bancada é desativada
        Returns:
            None
        """
        return 
    
    def ContextMenu(self, recipient):
        """Configura o menu de contexto
        
        Args: 
            recipient: O objeto que receberá o menu de contexto
        
        Returns:
            None
        """
        pass
        #self.appendContextMenu("EletroAlfa", self.list)

    def GetClassName(self)->str:
        """Retorna o tipo de classe da bancada.
        
        Returns:
            str: Identificador da classe FreeCAD
        """

        return "Gui::PythonWorkbench"

Gui.addWorkbench(Circuits())