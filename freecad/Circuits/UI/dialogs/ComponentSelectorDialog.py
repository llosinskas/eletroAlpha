"""
Diálogo reutilizável para seleção de componentes FreeCAD.
Permite buscar, visualizar e selecionar arquivos FCStd de uma pasta específica.
"""

import os
import zipfile
from pathlib import Path
from typing import Optional

from PySide import QtGui, QtCore
from PySide.QtGui import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide.QtGui import QScrollArea, QPushButton, QMessageBox
from PySide.QtCore import Qt, Signal, Slot
import FreeCAD as App
import FreeCADGui as Gui


class ComponentSelectorDialog(QDialog):
    """Diálogo para seleção de componentes com preview de thumbnails.
    
    Reutilizável para diferentes pastas de componentes.
    
    Attributes:
        components_path: Caminho da pasta contendo os componentes
        selected_component: Arquivo selecionado (retorna None se cancelado)
    
    Example:
        dialog = ComponentSelectorDialog(folder_path="Componentes/Eletrica")
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.selected_component
            # processar arquivo selecionado
    """
    
    # Signal emitido quando um componente é selecionado
    component_selected = Signal(str)  # emite o caminho do arquivo
    
    def __init__(self, components_path: str, title: str = "Selecionador de Componentes", parent=None):
        """Inicializa o diálogo.
        
        Args:
            components_path: Caminho da pasta com os componentes
            title: Título da janela do diálogo
            parent: Widget pai (para modality)
        """
        super().__init__(parent)
        
        self.components_path = components_path
        self.selected_component: Optional[str] = None
        
        self.initUI(title)
        self.load_components()
        
    def initUI(self, title: str):
        """Cria a interface do diálogo."""
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 900, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # Painel de busca
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite para filtrar componentes...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # Scroll Area com cards dos componentes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.components_container = QWidget()
        self.components_layout = QHBoxLayout(self.components_container)
        self.components_layout.setSpacing(12)
        self.components_layout.setContentsMargins(6, 6, 6, 6)
        
        scroll.setWidget(self.components_container)
        main_layout.addWidget(scroll)
        
        # Painel de info selecionado
        info_layout = QHBoxLayout()
        info_label = QLabel("Selecionado:")
        self.info_label = QLabel("Nenhum componente selecionado")
        self.info_label.setStyleSheet("color: #888; font-style: italic;")
        info_layout.addWidget(info_label)
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()
        main_layout.addLayout(info_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setEnabled(False)
        
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_ok)
        main_layout.addLayout(buttons_layout)
        
    def load_components(self):
        """Carrega os componentes da pasta especificada."""
        # Limpa componentes anteriores
        while self.components_layout.count():
            child = self.components_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.components_cards = {}
        
        if not os.path.exists(self.components_path):
            QMessageBox.warning(
                self, 
                "Erro",
                f"Pasta não encontrada: {self.components_path}"
            )
            return
        
        # Busca arquivos .FCStd (ignorando backup .FCBak)
        files = [
            f for f in os.listdir(self.components_path)
            if f.endswith('.FCStd')
        ]
        
        if not files:
            no_files = QLabel("Nenhum componente encontrado nesta pasta")
            no_files.setAlignment(Qt.AlignCenter)
            self.components_layout.addWidget(no_files)
            return
        
        # Cria um card para cada arquivo
        for filename in sorted(files):
            filepath = os.path.join(self.components_path, filename)
            card = ComponentCard(filename, filepath)
            card.clicked.connect(lambda checked=False, f=filepath: self.on_component_selected(f))
            self.components_cards[filepath] = card
            self.components_layout.addWidget(card)
        
        # Adiciona um spacer no final
        self.components_layout.addStretch()
        
    def on_component_selected(self, filepath: str):
        """Callback quando um componente é selecionado."""
        # Limpa seleção anterior
        for card in self.components_cards.values():
            card.set_selected(False)
        
        # Seleciona novo
        self.components_cards[filepath].set_selected(True)
        self.selected_component = filepath
        
        # Atualiza UI
        filename = os.path.basename(filepath)
        self.info_label.setText(filename)
        self.info_label.setStyleSheet("")
        self.btn_ok.setEnabled(True)
        
        # Emite signal
        self.component_selected.emit(filepath)
        
    def on_search_text_changed(self, text: str):
        """Filtra componentes conforme o usuário digita."""
        text_lower = text.lower()
        
        for card in self.components_cards.values():
            card.setVisible(text_lower in card.filename.lower())
    
    def get_selected_component(self) -> Optional[str]:
        """Retorna o caminho do componente selecionado ou None."""
        return self.selected_component


class ComponentCard(QWidget):
    """Card individual com thumbnail e informações do componente.
    
    Mostra thumbnail extraído do arquivo FCStd e nome do componente.
    """
    
    clicked = Signal()
    
    def __init__(self, filename: str, filepath: str, parent=None):
        """Inicializa o card.
        
        Args:
            filename: Nome do arquivo (ex: "Tomada.FCStd")
            filepath: Caminho completo do arquivo
            parent: Widget pai
        """
        super().__init__(parent)
        
        self.filename = filename
        self.filepath = filepath
        self.is_selected = False
        
        self.initUI()
        self.load_thumbnail()
        
    def initUI(self):
        """Cria a interface do card."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(120, 120)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setStyleSheet(
            "border: 2px solid #666; "
            "border-radius: 4px; "
            "background: #2b2b2b;"
        )
        
        # Nome do arquivo
        name_only = os.path.splitext(self.filename)[0]
        self.name_label = QLabel(name_only)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("font-size: 11px; color: #ddd;")
        
        layout.addWidget(self.thumbnail_label)
        layout.addWidget(self.name_label)
        
        self.setFixedWidth(140)
        self.setCursor(Qt.PointingHandCursor)
        
    def load_thumbnail(self):
        """Extrai e carrega o thumbnail do arquivo FCStd."""
        try:
            with zipfile.ZipFile(self.filepath, 'r') as z:
                # FreeCAD usa "thumbnails/Thumbnail.png" (t minúsculo)
                thumb_names = [n for n in z.namelist() if n.lower() == "thumbnails/thumbnail.png"]
                if thumb_names:
                    data = z.read(thumb_names[0])
                    pixmap = QtGui.QPixmap()
                    if pixmap.loadFromData(data):
                        scaled = pixmap.scaled(
                            115, 115,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                        self.thumbnail_label.setPixmap(scaled)
                        return
        except Exception as e:
            pass
        
        # Fallback: mostra icone genérico
        self.thumbnail_label.setText("📦")
        self.thumbnail_label.setStyleSheet(
            self.thumbnail_label.styleSheet() + "font-size: 48px;"
        )
        
    def mousePressEvent(self, event):
        """Emite signal quando clicado."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            
    def set_selected(self, selected: bool):
        """Marca/desmarca o card como selecionado."""
        self.is_selected = selected
        
        if selected:
            self.thumbnail_label.setStyleSheet(
                "border: 3px solid #4CAF50; "
                "border-radius: 4px; "
                "background: #2b2b2b;"
            )
            self.name_label.setStyleSheet(
                "font-size: 11px; color: #4CAF50; font-weight: bold;"
            )
        else:
            self.thumbnail_label.setStyleSheet(
                "border: 2px solid #666; "
                "border-radius: 4px; "
                "background: #2b2b2b;"
            )
            self.name_label.setStyleSheet("font-size: 11px; color: #ddd;")
