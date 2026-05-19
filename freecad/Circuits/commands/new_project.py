# Classe para criar um novo projeto elétrico. 
#  Copyright Lucas Losinskas 
# year 2023
import os 

try:
    from PySide2 import QtGui, QtCore, QtWidgets
except ImportError:
    try:
        from PySide6 import QtGui, QtCore, QtWidgets
    except ImportError:
        from PySide import QtGui, QtCore
        QtWidgets = QtGui

import FreeCADGui as Gui
import FreeCAD as App
import Spreadsheet

from freecad.Circuits.UI.insert_circuit import InsertCircuit
import freecad.Circuits as WB

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)
    

class newProjetctEletrical:
   
    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError('No active document found.\n')
            return 
        
        doc.addObject("App::DocumentObjectGroup", "Arquitetura_referencia")
        doc.addObject("App::DocumentObjectGroup", "Niveis")
        doc.addObject("App::DocumentObjectGroup", "Pontos_eletricos")
        doc.addObject("App::DocumentObjectGroup", "Quadros")
        doc.addObject("App::DocumentObjectGroup", "Tomadas")
        doc.addObject("App::DocumentObjectGroup", "Iluminacao")
        doc.addObject("App::DocumentObjectGroup", "Equipamentos")
        doc.addObject("App::DocumentObjectGroup", "Eletrodutos")
        doc.addObject("App::DocumentObjectGroup", "Eletrocalha")
        doc.addObject("App::DocumentObjectGroup", "Cabos")
        doc.addObject("App::DocumentObjectGroup", "Aterramento")
        doc.addObject("App::DocumentObjectGroup", "Tabelas_e_planilhas")
        doc.addObject("App::DocumentObjectGroup", "Detalhes")
        doc.addObject("App::DocumentObjectGroup", "Diagramas")
        doc.addObject("App::DocumentObjectGroup", "Projetos_2D")
                
        doc.recompute()

    def GetResources(self):
        return {'Pixmap': os.path.join(WB.ICON_PATH, 'newProject.svg'), 'MenuText': "Novo Projeto", 'ToolTip':"Iniciar um novo projeto"}

class CreateModel:

    def Activated(self):
        pasta_destino = os.path.join(WB.LIBRARY_PATH, "Eletrica")    
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        nome, ok = QtWidgets.QInputDialog.getText(None, "Salvar desenho", "Digite o nome do arquivo:")
        
        if ok and nome.strip():
            caminho = os.path.join(pasta_destino, nome.strip()+".FCStd")
            doc = App.newDocument(nome.strip())
            doc.addObject("App::DocumentObjectGroup", "Simbolo 2D")
            doc.addObject("App::DocumentObjectGroup", "Foto")
            doc.addObject("App::DocumentObjectGroup", "Modelo 3D")
            doc.addObject("App::DocumentObjectGroup", "Descricao")
            doc.addObject("App::DocumentObjectGroup", "Detalhes 2D")
            App.ActiveDocument.saveAs(caminho)
            
        else:
            QtWidgets.QMessageBox.warning(None, "Cancelado", "Operação cancelada")
                
        doc.recompute()

    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'add_model.svg'), 
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
        return {'Pixmap': os.path.join(WB.ICON_PATH, 'planilha.svg'), 'MenuText': "Nova Planilha", 'ToolTip':"Criar uma nova planilha de circuitos"}

class addCircuit(object):
    
    def Activated(self):
        form = InsertCircuit()
        form.exec_()
        
    def IsActive(self):
        return True
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'record-svgrepo-com.svg'), 
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
        
        pasta_destino = os.path.join(WB.LIBRARY_PATH, "Eletrica")    
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        else:
            arquivos = [f for f in os.listdir(pasta_destino) if f.endswith(".FCStd")]
            if not arquivos:
                QtWidgets.QMessageBox.information(None, "Nenhum arquivo", "Não há arquivos FCStd na pasta.")
            else:
                item, ok = QtWidgets.QInputDialog.getItem(None, "Abrir desenho", "Escolha o arquivo:", arquivos, editable=False)

                if ok:

                    doc = App.ActiveDocument
                    if doc is None:
                        App.Console.PrintError('No active document found.\n')
                        return 
                    caminho = os.path.join(pasta_destino, item)
                    item_sem = item.split(".")[0]
                    folder = doc.addObject("App::DocumentObjectGroup", item_sem)
                    doc2 = App.open(caminho)
                    
                    for obj in doc2.Objects:
                        if not listElements.is_name_equals(doc, obj):
                            copy = doc.copyObject(obj)
                            folder.addObject(copy)
                        
                    App.closeDocument(item_sem)
                    doc.recompute()
        
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'listElements.svg'), 
            'MenuText': "Listar Elementos", 
            'ToolTip':"Listar elementos elétricos"}


# Adiciona os camandos para o gerenciamento de comando do FreeCAD 
Gui.addCommand("newProjetctEletrical", newProjetctEletrical())
Gui.addCommand("newSpreadsheet", newSpreadsheet())
Gui.addCommand("AddSpreadsheet", addCircuit())
Gui.addCommand("ListElements", listElements())
Gui.addCommand("CreateModel", CreateModel())