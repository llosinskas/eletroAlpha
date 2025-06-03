

# Gerar o diagrama unifilar

import os
import FreeCADGui as Gui
import FreeCAD as App
import WorkbenchBase as WB
import Part 
import Draft
from PySide import QtWidgets

class GerarPlanilha:
    def gerar_tabela(self, doc):
        
        if not hasattr(doc, "QD"):

            planilha = doc.addObject('Spreadsheet::Sheet', 'QD')
            doc.recompute()
        else:
            planilha = doc.Spreadsheet("QD")
        planilha.set("A1", "Descrição")
        planilha.set("B1", "Tensão")
        planilha.set("C1", "n° de Fases")
        planilha.set("D1", "Terra?")
        planilha.set("E1", "Neutro?")
        planilha.set("F1", "DPS?")
        planilha.set("G1", "Potência total do quadro")
        planilha.set("H1", "Corrente nominal do disjuntor")
        planilha.set("I1", "Corrente de curto circuito")
        planilha.set("J1", "Curva do disjuntor")
        planilha.set("K1", "Classe do DPS")
        planilha.set("L1", "Tensão do DPS")
        planilha.set("M1", "Corrente do DPS")
        
        dialog = ParamDialog()
        if dialog.exec_():
            doc=App.activeDocument()


    def Activated(self):
        doc = App.activeDocument()
        GerarPlanilha.gerar_tabela(self, doc)

    def GetResources(self):
        # return {'Pixmap' : WB.IMAGE_PATH/"tomadas.svg", 'MenuText': "Gerar diagrama unifilar", "Tooltip":"Gerar um diagrama unifilar a partir dos dados inseridos no projeto"}
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'planilha.svg'), 'MenuText':'Gerar unifilar', 'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'}

class ParamDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dados do Quadro de distribuição")
        # self.layout = QtWidgets.QVBoxLayout()

        layout = QtWidgets.QFormLayout()
        self.descricao = QtWidgets.QLineEdit()
        self.tensao = QtWidgets.QLineEdit()
        self.n_fases = QtWidgets.QLineEdit()
        self.terra = QtWidgets.QLineEdit()
        self.neutro = QtWidgets.QLineEdit()
        self.pot_quadro = QtWidgets.QLineEdit()
        self.corrente_disjuntor = QtWidgets.QLineEdit()
        self.corrente_cc_disjuntor = QtWidgets.QLineEdit()
        self.classe_DPS = QtWidgets.QLineEdit()
        self.tensao_DPS = QtWidgets.QLineEdit()
        self.corrente_DPS = QtWidgets.QLineEdit()
        

        layout.addRow("Descrição do quadro de distribuição", self.descricao)
        layout.addRow("Tensão do quadro [V]", self.tensao)
        layout.addRow("Número de fases", self.n_fases)
        layout.addRow("terra?", self.terra)
        layout.addRow("neutro?", self.neutro)
        layout.addRow("Potência do quadro [kW]", self.pot_quadro)
        layout.addRow("Corrente nominal do disjuntor geral [A]", self.corrente_disjuntor)
        layout.addRow("Corrente de curto circuito do disjuntor geral [kA]", self.corrente_cc_disjuntor)
        layout.addRow("Classe do DPS", self.classe_DPS)
        layout.addRow("Tensão do DPS [V]", self.tensao_DPS)
        layout.addRow("Corrente do DPS[kA]", self.corrente_DPS)



        self.submit_btn = QtWidgets.QPushButton("Criar")
        self.cancel_btn = QtWidgets.QPushButton("Cancela")
        self.submit_btn.clicked.connect(self.accept)
        
        
        self.setLayout(layout)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.cancel_btn)
        
    


class GerarUnifilar:
    
    def gerar_tabela(self, doc):
        planilha = doc.addObject('Spreadsheet::Sheet', 'QD')
        planilha.set("A1", "Descrição")
        planilha.set("B1", "Tensão")
        planilha.set("C1", "n° de Fases")
        planilha.set("D1", "Terra?")
        planilha.set("E1", "Neutro?")
        planilha.set("F1", "DPS?")
        planilha.set("G1", "Potência total do quadro")
        planilha.set("H1", "Corrente nominal do disjuntor")
        planilha.set("I1", "Corrente de curto circuito")
        planilha.set("J1", "Curva do disjuntor")
        planilha.set("K1", "Classe do DPS")
        planilha.set("L1", "Tensão do DPS")
        planilha.set("M1", "Corrente do DPS")
        
        
        

    def pegar_tabela(self, doc):

        sheet = doc.Spreadsheet("QD")
        descricao = sheet.get("A2")
        tensao = sheet.get("B2")
        n_fases = sheet.get("C2")
        terra = sheet.get("D2")
        neutro = sheet.get("E2")
        dps = sheet.get("F2")
        potencia = sheet.get("G2")
        disjuntor = sheet.get("H2")
        corrente_cc_disjuntor =sheet.get("I2")
        curva_disjuntor = sheet.get("J2")
        classe_dps = sheet.get("K2")
        tensao_dps = sheet.get("L2")
        corrente_dps = sheet.get("M1")


    def gerar_linha(self,doc, potencia, dr, bitola, position, corrente, comprimento):
        sketch_body = doc.addObject("Sketcher::SketchObject", "Diagrama unifilar simples")
        sketch_body.Placement = position
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0,-comprimento/2),App.Vector(0, comprimento/2)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0,0),App.Vector(comprimento/2,0) ), False)
        if dr:
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,-comprimento/2), App.Vector(comprimento,-comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,-comprimento/2), App.Vector(comprimento/2,comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,comprimento/2), App.Vector(comprimento,comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento,-comprimento/2), App.Vector(comprimento,comprimento/2)), False)
            
            center_position = App.Vector(comprimento,comprimento)
            text = Draft.make_text(["DR"], placement =center_position , screen =None, height=None, line_spacing=None)
            print(text.Label)
            text.Label= "DR"
            Draft.autogroup(text)
        else:
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2, 0), App.Vector(comprimento, 0)), False)


        text = Draft.make_text([f"{potencia}"], placement = position, screen =None, height=None, line_spacing=None)
        Draft.autogroup(text)


    def Activated(self):
        doc = App.activeDocument()
        position = App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0))
        heigth =100
        GerarUnifilar.gerar_linha(self, doc, 100,True, 2.5,position, 30, heigth)




        doc.recompute()
    def IsActive(self):
        return True
    
    def GetResources(self):
        # return {'Pixmap' : WB.IMAGE_PATH/"tomadas.svg", 'MenuText': "Gerar diagrama unifilar", "Tooltip":"Gerar um diagrama unifilar a partir dos dados inseridos no projeto"}
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'unifilar.svg'), 'MenuText':'Gerar unifilar', 'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'}


Gui.addCommand("GerarUnifilar", GerarUnifilar()) 
Gui.addCommand("GerarPlanilha", GerarPlanilha())