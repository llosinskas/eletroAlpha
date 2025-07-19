# Classe para criar um novo projeto elétrico. 
#  Copyright Lucas Losinskas 
# year 2023


import os 
from PySide import QtGui, QtCore, QtWidgets
import FreeCADGui as Gui
import FreeCAD as App
import Spreadsheet
from UI.insert_circuit import InsertCircuit
import WorkbenchBase as WB

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
        pasta_destino = f"{WB.__dir__}/Componentes/Eletrica"    
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        nome, ok = QtGui.QInputDialog.getText(None, "Salvar desenho", "Digite o nome do arquivo:")
        
        if ok and nome.strip():
            caminho = os.path.join(pasta_destino, nome.strip()+".FCStd")
            doc = App.newDocument(nome.strip())
            folder = doc.addObject("App::DocumentObjectGroup", "Simbolo 2D")
            folder = doc.addObject("App::DocumentObjectGroup", "Foto")
            folder = doc.addObject("App::DocumentObjectGroup", "Modelo 3D")
            folder = doc.addObject("App::DocumentObjectGroup", "Descricao")
            folder = doc.addObject("App::DocumentObjectGroup", "Detalhes 2D")
            App.ActiveDocument.saveAs(caminho)
            
        else:
            QtGui.QMessageBox.warning(None, "Cancelado", "Operação cancelada")
                
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

    def is_descendant(child, parent):
        if child == parent:
            return True
        if hasattr(child, "Group"):
            for obj in child.Group:
                if listElements.is_descendant(obj, parent):
                    return True
        return False
    def is_name_equals(doc, objeto):
        for obj in doc.Objects:
            if obj.Label==objeto.Label:
                obj.Label = f"_{objeto.Label}"
                return True
        return False
    def Activated(self):
        
        pasta_destino = f"{WB.__dir__}/Componentes/Eletrica"    
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        else:
            arquivos = [f for f in os.listdir(pasta_destino) if f.endswith(".FCStd")]
            if not arquivos:
                QtGui.QMessageBox.information(None, "Nenhum arquivo", "Não há arquivos FCStd na pasta.")
            else:
                item, ok = QtGui.QInputDialog.getItem(None, "Abrir desenho", "Escolha o arquivo:", arquivos, editable=False)

                if ok:

                    doc = App.ActiveDocument
                    if doc is None:
                        App.Console.PrintError('No active document found.\n')
                        return 
                    caminho = os.path.join(pasta_destino, item)
                    # App.openDocument(caminho)
                    item_sem = item.split(".")[0]
                    folder = doc.addObject("App::DocumentObjectGroup", item_sem)
                    doc2 = App.open(caminho)
                    
                    for obj in doc2.Objects:
                        
                        
                        
                        if not listElements.is_name_equals(doc, obj):
                            if not folder.isChildOf(copy):    
                                copy = doc.copyObject(obj)
                                folder.addObject(copy)
                        
                        
                        # if hasattr(copy, 'getParentGroup'):
                            
                        #     if not listElements.is_descendant(obj, folder):
                        #         parent = copy.getParentGroup()
                            
                        #     if parent:
                        #         parent.removeObject(copy)                     
                        
                    App.closeDocument(item_sem)
                    doc.recompute()
    
                    

                    # doc.mergeProject(caminho)
                    
                    
                    
        
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