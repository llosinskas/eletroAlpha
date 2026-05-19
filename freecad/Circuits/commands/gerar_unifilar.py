
# Gerar o diagrama unifilar

import os
import FreeCADGui as Gui
import FreeCAD as App
import freecad.Circuits as WB
import Part 
import Draft
try:
    from PySide2 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
    except ImportError:
        from PySide import QtCore, QtGui
        QtWidgets = QtGui

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
            'Pixmap': os.path.join(WB.ICON_PATH, 'planilha.svg'),
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
        self.setMinimumWidth(350)
        
        layout = QtWidgets.QFormLayout()
        
        self.n_circuito = QtWidgets.QLineEdit()
        layout.addRow("Identificação (Nº):", self.n_circuito)
        
        self.destino = QtWidgets.QLineEdit()
        layout.addRow("Destino do Circuito:", self.destino)
        
        self.potencia = QtWidgets.QLineEdit()
        layout.addRow("Potência [W ou kW]:", self.potencia)
        
        self.tensao = QtWidgets.QComboBox()
        self.tensao.addItems(["127", "220", "380"])
        layout.addRow("Tensão [V]:", self.tensao)
        
        self.corrente = QtWidgets.QLineEdit()
        layout.addRow("Corrente de Projeto [A]:", self.corrente)
        
        self.cabo = QtWidgets.QComboBox()
        self.cabo.addItems(["1.5", "2.5", "4", "6", "10", "16", "25", "35", "50", "70", "95", "120"])
        layout.addRow("Bitola do Cabo [mm²]:", self.cabo)
        
        self.disjuntor = QtWidgets.QComboBox()
        self.disjuntor.addItems(["10", "16", "20", "25", "32", "40", "50", "63", "80", "100", "125"])
        layout.addRow("Corrente do Disjuntor [A]:", self.disjuntor)
        
        self.curva = QtWidgets.QComboBox()
        self.curva.addItems(["B", "C", "D"])
        layout.addRow("Curva do Disjuntor:", self.curva)
        
        fases_layout = QtWidgets.QHBoxLayout()
        self.fase_r = QtWidgets.QCheckBox("R")
        self.fase_s = QtWidgets.QCheckBox("S")
        self.fase_t = QtWidgets.QCheckBox("T")
        self.fase_r.setChecked(True)
        fases_layout.addWidget(self.fase_r)
        fases_layout.addWidget(self.fase_s)
        fases_layout.addWidget(self.fase_t)
        layout.addRow("Fases:", fases_layout)
        
        self.neutro = QtWidgets.QCheckBox("Possui Neutro")
        self.neutro.setChecked(True)
        layout.addRow("", self.neutro)
        
        self.terra = QtWidgets.QCheckBox("Possui Terra")
        self.terra.setChecked(True)
        layout.addRow("", self.terra)
        
        self.dr = QtWidgets.QCheckBox("Possui Proteção DR")
        layout.addRow("", self.dr)
        
        self.corrente_dr = QtWidgets.QLineEdit()
        self.corrente_dr.setPlaceholderText("Ex: 30mA")
        layout.addRow("Corrente do DR:", self.corrente_dr)

        self.submit_btn = QtWidgets.QPushButton("Adicionar Circuito")
        self.submit_btn.clicked.connect(self.accept)
        layout.addRow("", self.submit_btn)
        
        self.setLayout(layout)

    def get_dados(self):
        return {
            "N_circuito": self.n_circuito.text(),
            "Destino": self.destino.text(),
            "Potencia": self.potencia.text(),
            "Tensao": self.tensao.currentText(),
            "Corrente": self.corrente.text(),
            "Cabo": self.cabo.currentText(),
            "Disjuntor": self.disjuntor.currentText(),
            "Curva": self.curva.currentText(),
            "Fase_R": str(self.fase_r.isChecked()),
            "Fase_S": str(self.fase_s.isChecked()),
            "Fase_T": str(self.fase_t.isChecked()),
            "Neutro": str(self.neutro.isChecked()),
            "Terra": str(self.terra.isChecked()),
            "DR": str(self.dr.isChecked()),
            "Corrente_DR": self.corrente_dr.text()
        }

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

    def gerar_linha(self, doc, potencia, dr, bitola, position, corrente, comprimento, group):
        sketch_body = doc.addObject("Sketcher::SketchObject", "Circuito")
        sketch_body.Placement = position
        
        # Linha horizontal do circuito para a direita
        length = comprimento * 7
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0, 0), App.Vector(length, 0)), False)
        
        # Seta na ponta (direita)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(length, 0), App.Vector(length - comprimento/3, comprimento/4)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(length, 0), App.Vector(length - comprimento/3, -comprimento/4)), False)
        
        # Símbolo do disjuntor do circuito (cruzando a linha horizontal)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(length/5, -comprimento/4), App.Vector(length/5, comprimento/4)), False)
        
        if dr:
            # Símbolo do DR (retângulo)
            w = comprimento / 1.5
            h_dr = comprimento / 1.5
            x_dr = length/2
            sketch_body.addGeometry(Part.LineSegment(App.Vector(x_dr - w/2, -h_dr/2), App.Vector(x_dr + w/2, -h_dr/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(x_dr - w/2, h_dr/2), App.Vector(x_dr + w/2, h_dr/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(x_dr - w/2, -h_dr/2), App.Vector(x_dr - w/2, h_dr/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(x_dr + w/2, -h_dr/2), App.Vector(x_dr + w/2, h_dr/2)), False)
            
            GerarUnifilar.add_texto("DR", position.Base + App.Vector(x_dr, h_dr, 0), 0, comprimento/3, group)

        group.addObject(sketch_body)

        # Textos do circuito (Corrente, Bitola, Potência)
        y_text = comprimento / 3
        if corrente:
            GerarUnifilar.add_texto(f"{corrente}A", position.Base + App.Vector(length/5 + comprimento/4, y_text, 0), 0, comprimento/2.5, group)
        if bitola:
            GerarUnifilar.add_texto(f"#{bitola}", position.Base + App.Vector(length/2 - comprimento, y_text, 0), 0, comprimento/2.5, group)
        if potencia:
            GerarUnifilar.add_texto(f"{potencia}W", position.Base + App.Vector(length - comprimento*2, y_text, 0), 0, comprimento/2.5, group)

    def Activated(self):
        doc = App.activeDocument()
        heigth = 100     
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
            
            # Lê os circuitos a partir da linha 6 da planilha
            try:
                ultima_linha = GerarPlanilha.count_rows(quadro)
                if ultima_linha >= 6:
                    num_circuitos = 0
                    spacing = 5 * heigth
                    for row in range(6, ultima_linha + 1):
                        n_circuito = quadro.get(f"A{row}")
                        if not n_circuito:
                            continue
                            
                        destino = quadro.get(f"B{row}")
                        potencia = quadro.get(f"C{row}")
                        corrente = quadro.get(f"H{row}")
                        bitola_circ = quadro.get(f"J{row}")
                        # U = coluna 21 (DR) na lista corrigida: 
                        # N_circuito(0), Destino(1), Potência(2), Tensão(3), Fator(4), Comprimento(5), Aparente(6), Corrente(7),
                        # Queda(8), Cabo(9=J), Método(10), FatorAgrup(11), FatorTemp(12), Disj(13), Curva(14),
                        # R(15), S(16), T(17), Neutro(18), Terra(19), DR(20=U), CorrenteDR(21=V), Desc(22=W)
                        dr = str(quadro.get(f"U{row}")).lower() == "true"
                        
                        # Posição deste circuito no barramento (descendo em Y)
                        pos_circuito = App.Vector(18*heigth, 5/2*heigth - num_circuitos * spacing, 0)
                        
                        # Prolonga o barramento verticalmente
                        if num_circuitos > 0:
                            pos_anterior = App.Vector(18*heigth, 5/2*heigth - (num_circuitos - 1) * spacing, 0)
                            line_bus = Draft.make_line(pos_anterior, pos_circuito)
                            group.addObject(line_bus)
                            
                        # Gera a ramificação horizontal
                        pl_circ = App.Placement(pos_circuito, App.Rotation(0,0,0))
                        GerarUnifilar.gerar_linha(self, doc, potencia, dr, bitola_circ, pl_circ, corrente, heigth, group)
                        
                        # Identificação do Circuito e Destino (na ponta direita da linha)
                        length = heigth * 7
                        ponta = pos_circuito + App.Vector(length + heigth/2, 0, 0)
                        GerarUnifilar.add_texto(f"Circ. {n_circuito}", ponta + App.Vector(0, heigth/3, 0), 0, heigth*0.5, group)
                        if destino:
                            GerarUnifilar.add_texto(destino, ponta + App.Vector(0, -heigth/2, 0), 0, heigth*0.5, group)
                            
                        num_circuitos += 1
            except Exception as e:
                App.Console.PrintWarning(f"Não foi possível gerar os circuitos do quadro {quadro.Label}: {e}\n")
                
        doc.recompute()

    def IsActive(self):
        return True
    
    def GetResources(self):
        
        return {'Pixmap': os.path.join(WB.ICON_PATH, 'unifilar.svg'), 'MenuText':'Gerar unifilar', 'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'}

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
        quadros = get_quadros(self, doc)
        if not quadros:
            App.Console.PrintWarning("Nenhum quadro encontrado. Gere a planilha do quadro primeiro.\n")
            return
            
        dialog = Add_circuito()
        if dialog.exec_():
            dados = dialog.get_dados()
            
            for quadro in quadros:
                planilha = quadro
                header_sheet = [
                    "N_circuito", "Destino", "Potência [kW]", "Tensão [V]",
                    "Fator de potência", "Comprimento", "Potência Aparente [kVA]", "Corrente [A]", 
                    "Queda de tensão [%]", "Cabo [mm²]", "Método de instalação", "fator de agrupamento", "Fator de temperatura", 
                    "Disjuntor", "Curva disjuntor", 
                    "Fase R", "Fase S", "Fase T", "Neutro", "Terra",
                    "DR", "Corrente DR", "Descrição do Circuito"
                ]
                for index, header in enumerate(header_sheet):
                    coluna = chr(ord("A")+index)
                    planilha.set(f"{coluna}5", header)
                    
                ultima_linha = GerarPlanilha.count_rows(planilha)
                next_row = 6 if ultima_linha < 5 else ultima_linha + 1
                
                # Preenche a linha com os dados
                planilha.set(f"A{next_row}", f"'{dados['N_circuito']}")
                planilha.set(f"B{next_row}", f"'{dados['Destino']}")
                planilha.set(f"C{next_row}", f"'{dados['Potencia']}")
                planilha.set(f"D{next_row}", f"'{dados['Tensao']}")
                planilha.set(f"H{next_row}", f"'{dados['Corrente']}")
                planilha.set(f"J{next_row}", f"'{dados['Cabo']}")
                planilha.set(f"N{next_row}", f"'{dados['Disjuntor']}")
                planilha.set(f"O{next_row}", f"'{dados['Curva']}")
                planilha.set(f"P{next_row}", f"'{dados['Fase_R']}")
                planilha.set(f"Q{next_row}", f"'{dados['Fase_S']}")
                planilha.set(f"R{next_row}", f"'{dados['Fase_T']}")
                planilha.set(f"S{next_row}", f"'{dados['Neutro']}")
                planilha.set(f"T{next_row}", f"'{dados['Terra']}")
                planilha.set(f"U{next_row}", f"'{dados['DR']}")
                planilha.set(f"V{next_row}", f"'{dados['Corrente_DR']}")

        doc.recompute()

    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'adicionar.svg'), 
            'MenuText':'Adicionar um circuito no diagrama', 
            'ToolTip':'Adicionar um circuito no quadro'}

Gui.addCommand("AddCircuito", AddCircuito())
Gui.addCommand("GerarUnifilar", GerarUnifilar()) 
Gui.addCommand("GerarPlanilha", GerarPlanilha())