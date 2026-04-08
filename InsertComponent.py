"""
Comandos para inserção de componentes e elementos no projeto.
Utiliza o novo sistema reutilizável de seleção e inserção de componentes.
"""

import os
from pathlib import Path

import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui, QtCore
from PySide.QtGui import QMessageBox

from UI.dialogs import ComponentInserter


class InsertComponent:   
    """Comando para inserir componentes elétricos genéricos.
    
    Abre um diálogo para seleção de componentes de diversas categorias.
    """
  
    def Activated(self):
        """Ativado ao clicar no botão da barra de ferramentas."""
        doc = App.activeDocument()
        if not doc:
            QMessageBox.warning(
                None,
                "Erro",
                "Nenhum documento FreeCAD aberto.\nCrie um novo projeto primeiro."
            )
            return
        
        # Abre o selecionador de componentes
        folder = self._get_components_folder()
        inserter = ComponentInserter(
            folder,
            on_component_loaded=self._on_component_loaded
        )
        inserter.insert_component()
    
    def _get_components_folder(self) -> str:
        """Retorna o caminho da pasta de componentes."""
        base = Path(__file__).parent
        return str(base / "Componentes" / "Eletrica")
    
    def _on_component_loaded(self, filepath: str, obj):
        """Callback executado após carregar componente."""
        print(f"Componente inserido: {obj.Label}")
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'Componentes.svg'
            ), 
            'MenuText': 'Inserir novo circuito elétrico', 
            'ToolTip': 'Inserir um novo circuito elétrico'
        }


class Tugs:
    """Comando para inserir pontos de conexão de energia (tomadas).
    
    Abre diálogo selecionando tomadas disponíveis.
    """
    
    def Activated(self):
        """Ativado ao clicar no botão."""
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
        inserter.insert_component()
    
    def _get_components_folder(self) -> str:
        """Retorna pasta com componentes de tomadas."""
        base = Path(__file__).parent
        return str(base / "Componentes" / "Eletrica")
    
    def _on_component_loaded(self, filepath: str, obj):
        """Callback após inserir tomada."""
        print(f"Tomada inserida: {obj.Label}")
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'tomadas.svg'
            ), 
            'MenuText': 'Inserir ponto de conexão de energia', 
            'ToolTip': 'Inserir um novo ponto elétrico'
        }


class Equipaments:
    """Comando para inserir equipamentos elétricos.
    
    Exemplo: chuveiros, ar-condicionado, etc.
    """
    
    def Activated(self):
        """Ativado ao clicar no botão."""
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
        inserter.insert_component()
    
    def _get_components_folder(self) -> str:
        """Retorna pasta com equipamentos."""
        base = Path(__file__).parent
        return str(base / "Componentes" / "Eletrica")
    
    def _on_component_loaded(self, filepath: str, obj):
        """Callback após inserir equipamento."""
        print(f"Equipamento inserido: {obj.Label}")

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'equipamentos.svg'
            ), 
            'MenuText': 'Inserir um equipamento elétrico', 
            'ToolTip': 'Inserir um novo equipamento elétrico'
        }


class Wire:
    """Comando para inserir fiação."""
    
    def Activated(self):
        """Ativado ao clicar no botão."""
        doc = App.activeDocument()
        if not doc:
            QMessageBox.warning(
                None,
                "Erro",
                "Nenhum documento FreeCAD aberto."
            )
            return
        
        QMessageBox.information(
            None,
            "Funcionalidade",
            "Fiação será implementada em breve com traçado automático."
        )
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'fio.svg'
            ), 
            'MenuText': 'Inserir fiação', 
            'ToolTip': 'Inserir fiação no projeto'
        }


class Conduit:
    """Comando para inserir eletrodutos."""
    
    def Activated(self):
        """Ativado ao clicar no botão."""
        doc = App.activeDocument()
        if not doc:
            QMessageBox.warning(
                None,
                "Erro",
                "Nenhum documento FreeCAD aberto."
            )
            return
        
        QMessageBox.information(
            None,
            "Funcionalidade",
            "Eletrodutos serão implementados em breve com caminho parametrizado."
        )
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'conduite.svg'
            ), 
            'MenuText': 'Inserir conduite na instalação', 
            'ToolTip': 'Inserir conduite na instalação'
        }


class CableTray:
    """Comando para inserir eletrocalhas."""
    
    def Activated(self):
        """Ativado ao clicar no botão."""
        doc = App.activeDocument()
        if not doc:
            QMessageBox.warning(
                None,
                "Erro",
                "Nenhum documento FreeCAD aberto."
            )
            return
        
        QMessageBox.information(
            None,
            "Funcionalidade",
            "Eletrocalhas serão implementadas em breve."
        )
    
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "Resources/Icons", 
                'eletrocalha.svg'
            ), 
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

