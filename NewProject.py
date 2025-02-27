# Classe para criar um novo projeto elétrico. 
#  Copyright Lucas Losinskas 
# year 2023


import os 
from PySide import QtGui, QtCore, QtWidgets
import FreeCADGui as Gui
import FreeCAD as App
import Spreadsheet
from UI.insert_circuit import InsertCircuit

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    

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


class CreateModel:

    def Activated(self):
        doc = App.newDocument("Model")
        if doc is None:
            App.Console.PrintError('No active document found.\n')
            return 

        folder = doc.addObject("App::DocumentObjectGroup", "Simbolo 2D")
        folder = doc.addObject("App::DocumentObjectGroup", "Foto")
        folder = doc.addObject("App::DocumentObjectGroup", "Modelo 3D")
        folder = doc.addObject("App::DocumentObjectGroup", "Descricao")
        folder = doc.addObject("App::DocumentObjectGroup", "Detalhes 2D")
        
        
        
                
        doc.recompute()

    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'add_model.svg'), 
            'MenuText': "Criar Model", 'ToolTip':"Botão para criar Models"}



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

class addCircuit(object):
    
    
    def Activated(self):
        form = InsertCircuit()
   
        form.exec_()
        # doc = App.ActiveDocument
        
        # planilha =""
        # if doc.getObject("Circuitos"):
        #     planilha = doc.getObject("Circuitos")
        # else:
        #     newSpreadsheet.Activated(self)
        #     planilha = doc.getObject("Circuitos")

        
    def IsActive(self):
       
        return True
    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'record-svgrepo-com.svg'), 
            'MenuText': "Add Planilha", 
            'ToolTip':"Adicionar os circuitos na planilha"}

class listElements:
    def Activated(self):
        pass
    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)),"Resources/Icons", 'listElements.svg'), 
            'MenuText': "Listar Elementos", 
            'ToolTip':"Listar elementos elétricos"}



# Adiciona os camandos para o gerenciamento de comando do FreeCAD 
Gui.addCommand("newProjetctEletrical", newProjetctEletrical())
Gui.addCommand("newSpreadsheet", newSpreadsheet())
Gui.addCommand("AddSpreadsheet", addCircuit())
Gui.addCommand("ListElements", listElements())
Gui.addCommand("CreateModel", CreateModel())