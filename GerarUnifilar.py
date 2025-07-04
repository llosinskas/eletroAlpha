
# Gerar o diagrama unifilar

import os
import FreeCADGui as Gui
import FreeCAD as App
import WorkbenchBase as WB
import Part 
import Draft
from PySide import QtWidgets, QtCore

import re

class GerarPlanilha:
    def gerar_tabela(self, doc):
        
        dialog = CriarQuadro()
        if dialog.exec_():
            doc=App.activeDocument()

        dados = dialog.get_dados()
        nome_quadro = dados["indentificacao"]
        # nome_quadro='QD'
        if not hasattr(doc, nome_quadro):
            planilha = doc.addObject('Spreadsheet::Sheet', nome_quadro)
            doc.recompute()
        else:
            planilha = doc.Spreadsheet(nome_quadro)
        planilha.addProperty("App::PropertyString", "quadro")
        planilha.quadro = "Quadro"
        header_sheet = ["indentificacao_painel", "bitola", "origem","curto_circuito", "descricao","tensao", "numero_fases", "terra",
                    "neutro","curva_disjuntor",  "corrente_nominal_disjuntor", "corrente_curto_circuito", 
                    "potencia_instalada", "potencia_demanda", "material_quadro", 
                    "DPS", "classe_DPS", "tensao_DPS", "corrente_DPS"] 
        planilha.set("A1", nome_quadro)
        planilha.mergeCells('A1:S1')
        for index, header in enumerate(header_sheet):
            coluna = chr(ord('A')+index) 
            
            planilha.set(f"{coluna}2", header)
            planilha.setAlias(f"{coluna}3", header)
        planilha.set("A4","Circuitos")
        planilha.mergeCells('A4:S4')
        count = 0
        for index, value in dados.items():
            coluna = chr(ord('A')+count)
            planilha.set(f"{coluna}3", str(value))
            count+=1


        num_linhas = GerarPlanilha.count_rows(planilha)
        
    def count_rows(planilha):
        used = planilha.getUsedCells()
        linhas = [int(re.search(r'\d', cell).group()) for cell in used]
        ultima_linha = 0
        if linhas:
            ultima_linha = max(linhas)
        else:
            ultima_linha = 0
        return ultima_linha

    def Activated(self):
        doc = App.activeDocument()
        GerarPlanilha.gerar_tabela(self, doc)
        doc.recompute()
    
    def GetResources(self):
        
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'planilha.svg'),
            'MenuText':'Gerar unifilar', 
            'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'
            }

class CriarQuadro(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dados do Quadro de distribuição")
        
        layout = QtWidgets.QFormLayout()
        title1 = QtWidgets.QLabel("Informação do quadro")
        title1.setAlignment(QtCore.Qt.AlignCenter)
        layout.addRow(title1)         
        
        self.identificacao = QtWidgets.QLineEdit()
        self.identificacao.setPlaceholderText("Ex. QGBT, QD, QD01, QF01,...")
        layout.addRow("Identificação do quadro", self.identificacao)

        self.bitola = QtWidgets.QLineEdit()
        self.bitola.setPlaceholderText("Ex. 16, 25, 35,...")
        layout.addRow("Bitola do cabo de entrada [mm²]", self.bitola)

        self.origem = QtWidgets.QLineEdit()
        self.origem.setPlaceholderText("Ex. Padrão, QD1, QGBT, ...")
        layout.addRow("Origem", self.origem)

        self.curto = QtWidgets.QLineEdit()
        self.curto.setPlaceholderText("Ex. 3, 5, 6, ...")
        layout.addRow("Nível de curto circuito [kA]", self.curto)
        
        self.descricao = QtWidgets.QLineEdit()
        self.descricao.setPlaceholderText("Ex. Quadro de iluminação + tomadas, quadro de automação da iluminação")
        layout.addRow("Descrição do quadro", self.descricao)

        self.tensao = QtWidgets.QLineEdit()
        self.tensao.setPlaceholderText("Ex. 127, 220, 380")
        layout.addRow("Tensão de fase do quadro [V]", self.tensao)

        self.n_fases = QtWidgets.QComboBox()
        self.n_fases.addItems(["1", "2", "3"])
        self.n_fases.setPlaceholderText('Ex. 1,2,3')
        layout.addRow("Número de fases do quadro", self.n_fases)
        
        self.terra = QtWidgets.QCheckBox()
        layout.addRow("Tem terra no quadro?", self.terra)

        self.neutro = QtWidgets.QCheckBox()
        layout.addRow("Tem neutro no quadro", self.neutro)
        
        title2 = QtWidgets.QLabel("Disjuntor geral do quadro")
        title2.setAlignment(QtCore.Qt.AlignCenter)
        layout.addRow(title2)
        
        self.curva_disjuntor = QtWidgets.QComboBox()
        self.curva_disjuntor.addItems(["B", "C", "D"])
        layout.addRow("Curva do disjuntor geral", self.curva_disjuntor)

        self.corrente_nominal_disjuntor = QtWidgets.QLineEdit()
        self.corrente_nominal_disjuntor.setPlaceholderText("Ex. 10, 16, 20,...")
        layout.addRow("Corrente nominal do disjuntor geral do quadro [A]", self.corrente_nominal_disjuntor)

        self.corrente_cc_disjuntor = QtWidgets.QLineEdit()
        self.corrente_cc_disjuntor.setPlaceholderText("Ex. 3, 4, 16,...")
        layout.addRow("Corrente de curto circuito do disjuntor [kA]", self.corrente_cc_disjuntor)

        self.pot_quadro = QtWidgets.QLineEdit()
        self.pot_quadro.setPlaceholderText("Ex. 3,5,10,100,...")
        layout.addRow("Potência instalada do quadro [kW]", self.pot_quadro)

        self.demanda = QtWidgets.QLineEdit()
        self.demanda.setPlaceholderText("Ex. 3,4, 5, 100,...")
        layout.addRow("Demanda do quadro de distribuição [kW]", self.demanda)

        self.material = QtWidgets.QLineEdit()
        self.material.setPlaceholderText("Ex. Aço, ABS, Aço inox,...")
        layout.addRow("Material do quadro", self.material)

        self.dps = QtWidgets.QCheckBox()
        layout.addRow("Tem DPS", self.dps)

        self.classe_DPS = QtWidgets.QLineEdit()
        self.classe_DPS.setPlaceholderText("Ex. I, II, III, IV")
        layout.addRow("Classe do DPS", self.classe_DPS)

        self.tensao_DPS  = QtWidgets.QLineEdit()
        self.tensao_DPS.setPlaceholderText("Ex. 175, 275,...")
        layout.addRow("Tensão de operação do DPS [V]", self.tensao_DPS)

        self.corrente_DPS = QtWidgets.QLineEdit()
        self.corrente_DPS.setPlaceholderText("Ex. 3, 4, 5, ...")
        layout.addRow("Corrente do DPS [kA]", self.corrente_DPS)

        self.submit_btn = QtWidgets.QPushButton("Criar")
        
        self.submit_btn.clicked.connect(self.accept)
        
        self.setLayout(layout)
        layout.addWidget(self.submit_btn)
        
    
    def get_dados(self):
        dados = {
            "indentificacao": self.identificacao.text(), 
            "bitola_entrada": self.bitola.text(), 
            "origem": self.origem.text(), 
            "curto_circuito": self.curto.text(),
            "descricao":self.descricao.text(), 
            "tensao": self.tensao.text(), 
            "n_fases":self.n_fases.currentText(), 
            "terra":self.terra.isChecked(), 
            "neutro":self.neutro.isChecked(), 
            "curva_disjuntor":self.curva_disjuntor.currentText(), 
            "corrente_nominal_disjuntor":self.corrente_nominal_disjuntor.text(), 
            "corrente_cc_disjuntor": self.corrente_cc_disjuntor.text(), 
            "pot_quadro": self.pot_quadro.text(), 
            "demanda":self.demanda.text(), 
            "material":self.material.text(), 
            "dps":self.dps.isChecked(), 
            "classe_DPS":self.classe_DPS.text(), 
            "tensao_DPS":self.tensao_DPS.text(), 
            "corrente_DPS":self.corrente_DPS.text(), 
            }
        return dados

class Add_circuito(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Circuito")
        
        layout = QtWidgets.QFormLayout()
        self.descricao = QtWidgets.QLineEdit()

        layout.addRow("Descrição do circuito", self.descricao)

        self.setLayout(layout)


    def get_dados(self):
        dados = {}
        return dados

class GerarUnifilar:
         
    def cabo(doc, fase, terra, neutro, heigth, position, group):  
        
        # position = equipamento.Placement.Base
        sketch_body = doc.addObject('Sketcher::SketchObject', 'Cabo')
        sketch_body.Placement = App.Placement(position+App.Vector(50,50,0), App.Rotation(0,0,0)) 
        
        # Terra 
        if terra:
            sketch_body.addGeometry(Part.LineSegment(App.Vector(0, 0), App.Vector(0, heigth/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(-heigth/5, heigth/2), App.Vector(heigth/5, heigth/2)), False)
        
        if neutro:
            if terra:
                sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                sketch_body.addGeometry(Part.LineSegment(App.Vector(-heigth/5+heigth/2, heigth/2), App.Vector(heigth/2, heigth/2)), False)
                print("neutro com terra")
            else:
                sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                sketch_body.addGeometry(Part.LineSegment(App.Vector(-heigth/5, heigth/2), App.Vector(0, heigth/2)), False)
                print("neutro sem terra ")
        
        match fase:
            case 1:
                if neutro and terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                elif neutro or terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                else:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
            case 2:
                if neutro and terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                    
                elif neutro or terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                    
                else:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                    
            case 3:
                if neutro and terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth, -heigth/2), App.Vector(heigth+heigth, heigth/2)), False)
                elif neutro or terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                else:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)    
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
        group.addObject(sketch_body)

    def dps(doc, position, h, group):
        skecth = doc.addObject("Sketcher::SketchObject", 'dps')
        skecth.Placement=App.Placement(position, App.Rotation(0,0,0))
        p1 = App.Vector(0,0)
        p2 = App.Vector(0,-0.5*h)
        skecth.addGeometry(Part.LineSegment(p1, p2), False)
        q1 = App.Vector(-h, -0.5*h)
        q2 = App.Vector(h, -0.5*h)
        q3 = App.Vector(-h, -4*h)
        q4 = App.Vector(h, -4*h)
        skecth.addGeometry(Part.LineSegment(q1, q2), False)
        skecth.addGeometry(Part.LineSegment(q1, q3), False)
        skecth.addGeometry(Part.LineSegment(q2, q4), False)
        skecth.addGeometry(Part.LineSegment(q3, q4), False)
        
        t1 = App.Vector(-h/2, -h)
        t2 =App.Vector(h/2, -h)
        t3 = App.Vector(0,-2*h)
        skecth.addGeometry(Part.LineSegment(t1, t2), False)
        skecth.addGeometry(Part.LineSegment(t1, t3), False)
        skecth.addGeometry(Part.LineSegment(t2, t3), False)
        p1 = App.Vector(0, -4*h)
        p2 = App.Vector(0, -4.5*h)
        skecth.addGeometry(Part.LineSegment(p1, p2), False)
        
        p1 = App.Vector(-h/2, -4.5*h)
        p2 = App.Vector(h/2, -4.5*h)
        skecth.addGeometry(Part.LineSegment(p1, p2), False)
        p1 = App.Vector(-h/4, -4.75*h)
        p2 = App.Vector(h/4, -4.75*h)
        skecth.addGeometry(Part.LineSegment(p1, p2), False)
        p1 = App.Vector(-h/8, -5*h)
        p2 = App.Vector(h/8, -5*h)
        skecth.addGeometry(Part.LineSegment(p1, p2), False)
    

        group.addObject(skecth)

    def diagrama(self, doc,h, group, planilha):
        # Pegar valores da planilha 
        try:

            indentificacao_painel = planilha.get("indentificacao_painel")
            bitola = planilha.get("bitola")
            origem = planilha.get("origem")
            descricao = planilha.get("descricao")
            tensao = planilha.get("tensao")
            numero_fases=planilha.get("numero_fases")
            
            curva_disjuntor = planilha.get("curva_disjuntor")
            corrente_nominal_disjuntor = planilha.get("corrente_nominal_disjuntor")
            corrente_curto_circuito= planilha.get("corrente_curto_circuito")
            potencia_instalada = planilha.get("potencia_instalada")
            potencia_demanda= planilha.get("potencia_demanda")
            material_quadro = planilha.get("material_quadro")
            DPS = planilha.get("DPS")

            pos_texto = App.Vector(-h*0.5,0.5*h,0)
            GerarUnifilar.add_texto(origem, pos_texto, 90,h,  group)

            bitola = f"#{bitola}"
            pos_texto = App.Vector(5*h,h,0)
            GerarUnifilar.add_texto(bitola, pos_texto, 0,h,  group)

            disj = f"{curva_disjuntor} {corrente_nominal_disjuntor}A"
            pos_texto = App.Vector(10*h, 5*h, 0)
            GerarUnifilar.add_texto(disj,pos_texto, 0, h, group)

            disj_cc = f"{corrente_curto_circuito}kA"
            pos_texto = App.Vector(13*h, 3*h, 0)
            GerarUnifilar.add_texto(disj_cc,pos_texto, 0, h, group)

            descricao_label= f"Material: {material_quadro}"
            pos_texto = App.Vector(0, -2*h, 0)
            GerarUnifilar.add_texto(descricao_label,pos_texto, 0, h, group)
            
            pos_texto  = App.Vector(0, -3*h, 0)
            GerarUnifilar.add_texto(f"Potência Instalada:{potencia_instalada} kW",pos_texto, 0, h, group)

            pos_texto  = App.Vector(0, -4*h, 0)
            GerarUnifilar.add_texto(f"Demanda:{potencia_demanda} kW",pos_texto, 0, h, group)

            curto = planilha.get("curto_circuito")
            pos_texto = App.Vector(0, -5*h, 0)
            GerarUnifilar.add_texto(f"Nível de curto circuito no ponto {curto} kA", pos_texto, 0, h, group)
            
            descricao_label = f"{descricao}"
            pos_texto = App.Vector(0, -6*h, 0)
            GerarUnifilar.add_texto(descricao_label,pos_texto, 0, h, group)

            pos_texto = App.Vector(0, 5*h, 0)
            GerarUnifilar.add_texto(indentificacao_painel,pos_texto, 0, h, group)

            tensao_label = f"{tensao}V"
            pos_texto = App.Vector(5*h, 5*h, 0)
            GerarUnifilar.add_texto(tensao_label,pos_texto, 0, h, group)

           
            classe_DPS = ""
            tensao_DPS = ""
            corrente_DPS = ""
            if DPS == "True":
                classe_DPS = planilha.get("classe_DPS")
                tensao_DPS = planilha.get("tensao_DPS")
                corrente_DPS = planilha.get("corrente_DPS")
                
                pl = App.Vector(15*h, 5/2*h, 0)
                GerarUnifilar.dps(doc, pl, h, group)
                
                pl = App.Vector(h*17, 0,0)
                GerarUnifilar.add_texto(f"Classe: {classe_DPS}",pl, 0, h, group)
                pl = App.Vector(h*17, -h,0)
                GerarUnifilar.add_texto(f"{tensao_DPS}V",pl, 0, h, group)
                pl = App.Vector(h*17, -2*h,0)
                GerarUnifilar.add_texto(f"{corrente_DPS}kA",pl, 0, h, group)

        except Exception as e:
            print(f"Erro ao acessar o valor da planilha do quadro: {e}")
        
        # Linha 
        p1 = App.Vector(0,0,0)
        p2 = App.Vector(0, 5*h, 0)
        line = Draft.make_line(p1, p2)
        group.addObject(line)
        p1 = App.Vector(0, 5/2*h, 0)
        p2 = App.Vector(10*h, 5/2*h, 0)
        line = Draft.make_line(p1, p2)
        group.addObject(line)
        p1 = App.Vector(13*h, 5/2*h, 0)
        p2 = App.Vector(18*h, 5/2*h, 0)
        line = Draft.make_line(p1, p2)
        group.addObject(line)

        # Terminal disjuntor
        pl = App.Placement()
        pl.Base = App.Vector(10*h, 5/2*h,0)
        circle = Draft.make_circle(radius=h/10, placement=pl, face=True, support=None)
        group.addObject(circle)
        pl.Base = App.Vector(13*h, 5/2*h,0)
        circle = Draft.make_circle(radius=h/10, placement=pl, face=True, support=None)
        group.addObject(circle)

        pl.Base=App.Vector(11.5*h, 5/2*h,0)
        circle = Draft.make_circle(radius=1.5*h, placement=pl, startangle=0, endangle=180)
        group.addObject(circle)
        
        neutro = planilha.get("neutro")
        terra = planilha.get("terra")
        neutro_bool = False
        terra_bool = False
        if neutro == "True":
            neutro_bool=True
        if terra == "True":
            terra_bool=True

        pl.Base = App.Vector(5*h, 2*h, 0)
        GerarUnifilar.cabo(doc, numero_fases, terra_bool, neutro_bool, h, pl.Base, group)
        
        fator = 1
        match numero_fases:
            case 1:
                fator = 0
            case 2:
                fator = -0.25
            case 3:
                fator = -0.5
        pl.Base = App.Vector(11*h+fator*h, 3.5*h, 0)
        GerarUnifilar.cabo(doc,numero_fases, False, False, h, pl.Base, group)
    
    def add_texto(text, position, angle, h, group):
        texto = Draft.make_text(str(text), placement = position, screen=None, height=h, line_spacing=None)
        texto.Placement.Rotation = App.Rotation(App.Vector(0,0,1), angle)
        # Draft.rotate([texto],angle, position, App.Vector(0,0,1),copy=False)
        group.addObject(texto)

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
        heigth =100     
        quadros = []
        quadros = get_quadros(self, doc)

        for index, quadro in enumerate(quadros):
            diagrama_label = f"diagrama_{quadro.Label}"
            diagrama = doc.getObject(diagrama_label)
            if diagrama:
                diagrama.removeObjectsFromDocument()
                doc.removeObject(diagrama_label)
                doc.recompute()         
            group = doc.addObject("App::DocumentObjectGroup", f"diagrama {quadro.Label}")
            GerarUnifilar.diagrama(self, doc, heigth, group, quadro)
        doc.recompute()

    def IsActive(self):
        return True
    
    def GetResources(self):
        
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'unifilar.svg'), 'MenuText':'Gerar unifilar', 'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'}

def get_quadros(self, doc):
    quadros = []
    for obj in doc.Objects:
        if hasattr(obj, "quadro"):
            quadros.append(obj)
    if len(quadros) == 0:
        GerarPlanilha.Activated(self)
            
    return quadros

class AddCircuito:
    def Activated(self):
        doc = App.activeDocument()
        height = 100
        quadros = get_quadros(self, doc)
        for quadro in quadros:
            dialog = Add_circuito()
            if dialog.exec_():
                doc=App.activeDocument()
            planilha = quadro
            header_sheet = [
                "N_circuito", "Destino", "Potência [kW]", "Tensão [V]"
                "Fator de potência","Comprimento", "Potência Aparente [kVA]", "Corrente [A]", 
                "Queda de tensão [%]", "Cabo [mm²]", "Médo de instalação", "fator de agrupamento", "Fator de temperatura", 
                "Disjuntor", "Curva disjuntor", 
                "Fase R", "Fase S", "Fase T", "Neutro", "Terra"
                "DR", "Corrente DR", "Descrição do Circuito"]
            for index, header in enumerate(header_sheet):
                coluna = chr(ord("A")+index)
                planilha.set(f"{coluna}5", header)


        doc.recompute()

    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'adicionar.svg'), 
            'MenuText':'Adicionar um circuito no diagrama', 
            'ToolTip':'Adicionar um circuito no quadro'}

Gui.addCommand("AddCircuito", AddCircuito())
Gui.addCommand("GerarUnifilar", GerarUnifilar()) 
Gui.addCommand("GerarPlanilha", GerarPlanilha())