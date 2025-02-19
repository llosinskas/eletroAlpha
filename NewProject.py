# Classe para criar um novo projeto elétrico. 
#  Copyright Lucas Losinskas 
# year 2023


import os 
from PySide import QtGui, QtCore
import FreeCADGui as Gui
import FreeCAD as App
import Spreadsheet


class newProjetctEletrical:
   
   
    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError('No active document found.\n')
            return 

        folder = doc.addObject("App::DocumentObjectGroup", "Projeto 3D")
        folder = doc.addObject("App::DocumentObjectGroup", "Projeto 2D")
        folder = doc.addObject("App::DocumentObjectGroup", "Equipamentos")
                
        doc.recompute()

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'newProject.svg'), 'MenuText': "Novo Projeto", 'ToolTip':"Iniciar um novo projeto"}


class newSpreadsheet:
    def Activated(self):
        doc= App.ActiveDocument
        planilha = doc.addObject('Spreadsheet::Sheet', 'Circuitos')
        planilha.set('A1', 'ID') 
        planilha.set('B1', 'Origem') 
        planilha.set('C1', 'Destino')
        planilha.set('D1', 'Potência (kW)')  
        planilha.set('E1', 'Tensão (V)')
        planilha.set('F1', 'Fator de potência')
        planilha.set('G1', 'Potência aparente (kVA)')
        planilha.set('H1', 'Corrente (A)')
        planilha.set('I1', 'Comprimento do circuito (m)')
        planilha.set('J1', '% de queda de tensão ')
        planilha.set('K1', 'Secção do cabo mm²')
        planilha.set('L1', 'Método de instalação')
        planilha.set('M1', 'Fator de agrupamento')
        planilha.set('N1', 'Fator de temperatura')
        planilha.set('O1', 'Disjutor (A)')
        planilha.set('P1', 'Curva do disjuntor')
        planilha.set('Q1', 'Fase R')
        planilha.set('R1', 'Fase S')
        planilha.set('S1', 'Fase T')
        App.ActiveDocument.recompute()
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'planilha.svg'), 'MenuText': "Nova Planilha", 'ToolTip':"Criar uma nova planilha de circuitos"}

# Adiciona os camandos para o gerenciamento de comando do FreeCAD 
Gui.addCommand("newProjetctEletrical", newProjetctEletrical())
Gui.addCommand("newSpreadsheet", newSpreadsheet())