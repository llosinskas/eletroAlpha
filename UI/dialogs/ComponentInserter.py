"""
Gerenciador de inserção de componentes FreeCAD.
Controla o fluxo de seleção e posicionamento de componentes no documento.
"""

import os
from typing import Optional, Callable, Any

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore
from PySide.QtGui import QMessageBox, QDialog

from .ComponentSelectorDialog import ComponentSelectorDialog


class ComponentInserter:
    """Gerenciador de inserção de componentes no documento FreeCAD.
    
    Orquestra todo o processo: diálogo de seleção, abertura do componente,
    e inserção no documento ativo.
    
    Attributes:
        components_folder: Pasta onde estão os componentes
        on_component_loaded: Callback executado após carregar o componente
    
    Example:
        inserter = ComponentInserter("Componentes/Eletrica")
        inserter.insert_component()
    """
    
    def __init__(
        self, 
        components_folder: str,
        on_component_loaded: Optional[Callable[[str, Any], None]] = None,
        parent: Optional[QtGui.QWidget] = None
    ):
        """Inicializa o gerenciador.
        
        Args:
            components_folder: Caminho da pasta com componentes
            on_component_loaded: Callback(filepath, freecad_object) executado 
                                 após carregar o componente
            parent: Widget pai para o diálogo
        """
        self.components_folder = components_folder
        self.on_component_loaded = on_component_loaded
        self.parent = parent
        self.loaded_component = None
        
    def insert_component(self) -> bool:
        """Abre o diálogo de seleção e insere o componente.
        
        Returns:
            True se inserido com sucesso, False se cancelado/erro
        """
        # Valida documento ativo
        if not App.activeDocument():
            QMessageBox.warning(
                self.parent,
                "Erro",
                "Nenhum documento FreeCAD aberto.\nCrie ou abra um projeto primeiro."
            )
            return False
        
        # Abre diálogo de seleção
        dialog = ComponentSelectorDialog(
            self.components_folder,
            title="Selecionar Componente",
            parent=self.parent
        )
        
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selected_component()
            if selected:
                return self.load_and_insert_component(selected)
        
        return False
    
    def load_and_insert_component(self, filepath: str) -> bool:
        """Carrega e insere um componente específico.
        
        Args:
            filepath: Caminho completo do arquivo FCStd to inserir
            
        Returns:
            True se bem-sucedido
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
            
            doc = App.activeDocument()
            
            # Abre o componente em um documento temporário
            component_doc = App.open(filepath)
            
            if not component_doc:
                raise RuntimeError(f"Falha ao abrir: {filepath}")
            
            if not component_doc.Objects:
                App.closeDocument(component_doc.Name)
                raise RuntimeError("Nenhum objeto encontrado no componente")
            
            # Usa mergeProject para importar TODOS os objetos com estrutura completa
            App.setActiveDocument(doc.Name)
            doc.mergeProject(filepath)
            
            # Salva label do primeiro objeto para referência
            component_label = component_doc.Objects[0].Label if component_doc.Objects else "Componente"
            self.loaded_component = component_label
            
            # Fecha documento temporário
            App.closeDocument(component_doc.Name)
            
            # Recomputa
            doc.recompute()
            
            # Callback - passa o último objeto adicionado ao doc
            if self.on_component_loaded:
                last_obj = doc.Objects[-1] if doc.Objects else None
                self.on_component_loaded(filepath, last_obj)
            
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Erro ao Inserir Componente",
                f"Falha ao inserir componente:\n\n{str(e)}"
            )
            return False
    
    def _get_main_component_object(self, doc):
        """Identifica o objeto principal do componente.
        
        Procura por objetos visíveis primeiro, depois retorna o primeiro
        objeto não-documento encontrado.
        """
        # Prioriza grupos com objetos
        for obj in doc.Objects:
            if obj.TypeId == 'App::DocumentObjectGroup':
                if obj.Group:  # Se o grupo tem objetos dentro
                    return obj
        
        # Ou retorna o primeiro objeto visível/renderizável
        for obj in doc.Objects:
            if hasattr(obj, 'Shape') or obj.TypeId in [
                'App::DocumentObjectGroup',
                'Part::FeaturePython',
                'Part::Feature'
            ]:
                return obj
        
        # Fallback: primeiro objeto qualquer
        return doc.Objects[0]if doc.Objects else None
    
    def insert_component_with_placement(self, filepath: str) -> bool:
        """Insere componente permitindo ajustar a posição com o mouse.
        
        Após inserir, ativa modo interativo onde o usuário pode clicar
        para definir a posição final do componente.
        
        Args:
            filepath: Caminho do arquivo FCStd
            
        Returns:
            True se bem-sucedido
        """
        if not self.load_and_insert_component(filepath):
            return False
        
        # Aqui poderia ter lógica adicional para posicionamento
        # Por enquanto, apenas insere no origin
        return True
    
    def insert_multiple_components(self, filepaths: list) -> int:
        """Insere múltiplos componentes.
        
        Args:
            filepaths: Lista de caminhos de arquivos FCStd
            
        Returns:
            Número de componentes inseridos com sucesso
        """
        count = 0
        for filepath in filepaths:
            if self.load_and_insert_component(filepath):
                count += 1
        
        return count


class ComponentInsertionMode:
    """Modo interativo para inserção de componentes com mouse.
    
    Permite que o usuário clique no documento para posicionar componentes.
    """
    
    def __init__(self, component_filepath: str):
        """Inicializa o modo de inserção.
        
        Args:
            component_filepath: Caminho do componente a inserir
        """
        self.component_filepath = component_filepath
        self.is_active = False
        self._old_callback = None
        
    def start(self):
        """Ativa o modo de inserção com mouse."""
        view = Gui.ActiveDocument.ActiveView
        if not view:
            return
        
        self.is_active = True
        # Aqui se configuraria callbacks para mouse events do FreeCAD
        # Depende da versão do FreeCAD e sua API de eventos
        
    def stop(self):
        """Desativa o modo de inserção."""
        self.is_active = False
        # Restauraria callbacks anteriores
