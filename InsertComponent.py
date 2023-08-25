import os 
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui


import Eletro_locator
import core.EletroGui as EletroGui


class InsertComponent:   

    def Activated(self):
        doc=App.activeDocument()
        form = EletroGui.MainDialog()
        form.exec_()
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'Componentes.svg'), 'MenuText':'Inserir novo circuito elétrico', 'ToolTip':'Inserir um novo circuito elétrico elétrico'}


class Tugs:
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'tomadas.svg'), 'MenuText':'Inserir ponto de conexão de energia', 'ToolTip':'Inserir um novo ponto elétrico'}


class Equipaments:
    
    def Activated(self):
        doc=App.activeDocument()
        body = doc.addObject("App::DocumentObjectGroup", 'Projeto_3D')
        caixa = doc.addObject('Part::Box', 'MinhaCaixa')
        caixa.Length = 10
        caixa.Width = 20
        caixa.Height = 30
        body.addObject(caixa)

        App.ActiveDocument.recompute()


    def GetResources(self):
        
        
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'equipamentos.svg'), 'MenuText':'Inserir um equipamento elétrico', 'ToolTip':'Inserir um novo equipamento elétrico'}


class Wire:
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'fio.svg'), 'MenuText':'Inserir fiação', 'ToolTip':'Inserir fiação no projeto'}


class Conduit:
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'conduite.svg'), 'MenuText':'Inserir conduite na instalação', 'ToolTip':'Inserir conduite na instalação'}


class CableTray:
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'eletrocalha.svg'), 'MenuText':'Inserir eletrocalha na instalação', 'ToolTip':'Inserir eletrocalha na instalação'}




Gui.addCommand("InsertComponent", InsertComponent())
Gui.addCommand("InsertTugs", Tugs())
Gui.addCommand("InsertEquipaments", Equipaments())
Gui.addCommand("InsertWire", Wire())
Gui.addCommand("InsertConduit", Conduit())
Gui.addCommand("InsertCableTray", CableTray())
