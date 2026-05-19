"""
Comandos para inserção de componentes e elementos no projeto.
Utiliza o novo sistema reutilizável de seleção e inserção de componentes.
"""

import os
from pathlib import Path

import FreeCADGui as Gui
import FreeCAD as App
import freecad.Circuits as WB

try:
    from PySide2 import QtGui, QtCore, QtWidgets
except ImportError:
    try:
        from PySide6 import QtGui, QtCore, QtWidgets
    except ImportError:
        from PySide import QtGui, QtCore
        QtWidgets = QtGui

from freecad.Circuits.UI.dialogs import ComponentInserter


class InsertComponent:   
    """Comando para inserir componentes elétricos genéricos."""
  
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(
                None,
                "Erro",
                "Nenhum documento FreeCAD aberto."
            )
            return
        
        folder = self._get_components_folder()
        inserter = ComponentInserter(
            folder,
            on_component_loaded=self._on_component_loaded
        )
        inserter.insert_component_as_link_with_placement()
    
    def _get_components_folder(self) -> str:
        return WB.LIBRARY_PATH
    
    def _on_component_loaded(self, filepath: str, obj):
        print(f"Componente inserido: {obj.Label}")
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'Componentes.svg'), 
            'MenuText': 'Inserir novo circuito elétrico', 
            'ToolTip': 'Inserir um novo circuito elétrico'
        }


class Tugs:
    """Comando para inserir pontos de conexão de energia (tomadas).
    
    Utiliza App::Link (make link) para criar referências ao componente
    original, organizando tudo dentro de uma pasta no documento ativo.
    Permite posicionamento interativo com o mouse.
    """
    
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum documento FreeCAD aberto.")
            return
        
        folder = self._get_components_folder()
        inserter = ComponentInserter(
            folder,
            on_component_loaded=self._on_component_loaded
        )
        inserter.insert_component_as_link_with_placement()
    
    def _get_components_folder(self) -> str:
        return os.path.join(WB.LIBRARY_PATH, "Eletrica")
    
    def _on_component_loaded(self, filepath: str, obj):
        print(f"Tomada inserida (link com posicionamento): {obj.Label}")
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'tomadas.svg'), 
            'MenuText': 'Inserir ponto de conexão de energia', 
            'ToolTip': 'Inserir um novo ponto elétrico'
        }


class Equipaments:
    """Comando para inserir equipamentos elétricos.
    
    Permite posicionamento interativo com o mouse.
    """
    
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum documento FreeCAD aberto.")
            return
        
        folder = self._get_components_folder()
        inserter = ComponentInserter(
            folder,
            on_component_loaded=self._on_component_loaded
        )
        inserter.insert_component_as_link_with_placement()
    
    def _get_components_folder(self) -> str:
        return os.path.join(WB.LIBRARY_PATH, "Eletrica")
    
    def _on_component_loaded(self, filepath: str, obj):
        print(f"Equipamento inserido (link com posicionamento): {obj.Label}")

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'equipamentos.svg'), 
            'MenuText': 'Inserir um equipamento elétrico', 
            'ToolTip': 'Inserir um novo equipamento elétrico'
        }


class Wire:
    """Comando para inserir fiação."""
    
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum documento FreeCAD aberto.")
            return
        
        QtWidgets.QMessageBox.information(
            None,
            "Funcionalidade",
            "Fiação será implementada em breve com traçado automático."
        )
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'fio.svg'), 
            'MenuText': 'Inserir fiação', 
            'ToolTip': 'Inserir fiação no projeto'
        }

class Conduit:
    """Comando para iniciar o desenho do caminho dos eletrodutos usando Draft Wire nativo."""
    
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum documento FreeCAD aberto.")
            return
            
        App.Console.PrintMessage("Ferramenta de Eletroduto ativada. Desenhe a linha base usando as propriedades de Wire do FreeCAD.\n")
        Gui.runCommand('Draft_Wire')
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'conduite.svg'), 
            'MenuText': 'Desenhar Eletroduto (Draft Wire)', 
            'ToolTip': 'Desenha a linha guia do eletroduto usando a ferramenta nativa de Wire'
        }


class CableTray:
    """Comando para inserir eletrocalhas."""
    
    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum documento FreeCAD aberto.")
            return
        
        QtWidgets.QMessageBox.information(
            None,
            "Funcionalidade",
            "Eletrocalhas serão implementadas em breve."
        )
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(WB.ICON_PATH, 'eletrocalha.svg'), 
            'MenuText': 'Inserir eletrocalha na instalação', 
            'ToolTip': 'Inserir eletrocalha na instalação'
        }


# Registra os comandos no FreeCAD
Gui.addCommand("InsertComponent", InsertComponent())
Gui.addCommand("InsertTugs", Tugs())
Gui.addCommand("InsertEquipaments", Equipaments())
Gui.addCommand("InsertWire", Wire())
Gui.addCommand("InsertConduit", Conduit())
Gui.addCommand("InsertCableTray", CableTray())
