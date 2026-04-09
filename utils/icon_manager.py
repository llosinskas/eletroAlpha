"""
Gerenciador de ícones com suporte para temas light/dark.

Este módulo detecta o tema ativo do FreeCAD e aplica estilos apropriados aos ícones SVG,
adicionando contorno branco para melhor visibilidade no modo dark.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple, Optional


class IconManager:
    """Gerencia ícones com suporte para temas light/dark do FreeCAD."""
    
    # Namespace SVG
    SVG_NS = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', SVG_NS)
    
    def __init__(self, icon_dir: Optional[str] = None):
        """
        Inicializa o gerenciador de ícones.
        
        Args:
            icon_dir: Diretório contendo os ícones (padrão: Resources/Icons)
        """
        if icon_dir is None:
            module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_dir = os.path.join(module_dir, 'Resources', 'Icons')
        
        self.icon_dir = icon_dir
        self.is_dark_theme = self._detect_dark_theme()
    
    @staticmethod
    def _detect_dark_theme() -> bool:
        """
        Detecta se o tema dark do FreeCAD está ativo.
        
        Returns:
            True se o tema é dark, False caso contrário
        """
        try:
            import FreeCADGui
            # Verifica se o background é escuro
            palette = FreeCADGui.getMainWindow().palette()
            bg_color = palette.color(palette.Window)
            # Se a luminância é baixa, é tema dark
            luminance = (0.299 * bg_color.red() + 0.587 * bg_color.green() + 0.114 * bg_color.blue())
            return luminance < 128
        except:
            # Padrão: considerar light theme se não conseguir detectar
            return False
    
    def enhance_svg_for_dark_theme(self, svg_path: str) -> str:
        """
        Aprimora um ícone SVG adicionando contorno branco para tema dark.
        
        Args:
            svg_path: Caminho do arquivo SVG
            
        Returns:
            Caminho do arquivo SVG modificado (mesmo arquivo, modificado in-place)
        """
        if not os.path.exists(svg_path):
            return svg_path
        
        try:
            # Parse SVG
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Adiciona estilo global que aplica stroke branco
            style_elem = root.find('style')
            if style_elem is None:
                style_elem = ET.Element('style')
                root.insert(0, style_elem)
            
            # Estilo que adiciona contorno branco a todos os elementos
            dark_theme_style = """
                svg { filter: drop-shadow(0 0 0.5px white); }
                path, circle, ellipse, rect, polygon, polyline, line { 
                    stroke-width: 1.2; 
                    filter: drop-shadow(-0.5px -0.5px 0 white) drop-shadow(0.5px -0.5px 0 white) drop-shadow(-0.5px 0.5px 0 white) drop-shadow(0.5px 0.5px 0 white);
                }
            """
            style_elem.text = dark_theme_style
            
            # Salva SVG modificado
            tree.write(svg_path, encoding='UTF-8', xml_declaration=True)
            
            return svg_path
        except Exception as e:
            print(f"Erro ao modificar {svg_path}: {e}")
            return svg_path
    
    def add_white_stroke_to_all_icons(self) -> Tuple[int, int]:
        """
        Adiciona contorno branco a todos os ícones SVG no diretório.
        
        Returns:
            Tupla (total_arquivos, arquivos_modificados)
        """
        success_count = 0
        total_count = 0
        
        if not os.path.exists(self.icon_dir):
            print(f"Diretório {self.icon_dir} não encontrado")
            return 0, 0
        
        # Processa todos os SVG
        for filename in os.listdir(self.icon_dir):
            if filename.endswith('.svg'):
                total_count += 1
                svg_path = os.path.join(self.icon_dir, filename)
                
                try:
                    self.enhance_svg_for_dark_theme(svg_path)
                    success_count += 1
                    print(f"✓ {filename}")
                except Exception as e:
                    print(f"✗ {filename}: {e}")
        
        return total_count, success_count
    
    def get_icon_path(self, icon_name: str) -> str:
        """
        Retorna o caminho para um ícone.
        
        Args:
            icon_name: Nome do ícone (ex: 'logo.svg')
            
        Returns:
            Caminho absoluto do ícone
        """
        return os.path.join(self.icon_dir, icon_name)
    
    @staticmethod
    def apply_dark_theme_filter_to_pixmap(pixmap):
        """
        Aplica filtro de tema escuro a um QPixmap (alternativa).
        
        Args:
            pixmap: QPixmap do PySide
            
        Returns:
            QPixmap com filtro aplicado
        """
        try:
            from PySide import QtGui
            
            # Cria imagem com invertidas cores se no tema dark
            image = pixmap.toImage()
            
            # Inverte cores para melhor visibilidade
            for y in range(image.height()):
                for x in range(image.width()):
                    rgba = image.pixel(x, y)
                    color = QtGui.QColor(rgba)
                    
                    # Adiciona branco se for muito escuro
                    if color.lightness() < 100:
                        color.setAlpha(min(255, color.alpha() + 50))
                    
                    image.setPixel(x, y, color.rgba())
            
            return QtGui.QPixmap.fromImage(image)
        except:
            return pixmap


def initialize_dark_theme_icons():
    """Inicializa ícones com suporte a tema dark."""
    manager = IconManager()
    
    if manager.is_dark_theme:
        print("Tema dark detectado - aprimorando ícones...")
        total, success = manager.add_white_stroke_to_all_icons()
        print(f"Ícones processados: {success}/{total}")
    else:
        print("Tema light detectado - usando ícones padrão")


if __name__ == '__main__':
    # Teste: executar como script para aprimorar todos os ícones
    manager = IconManager()
    total, success = manager.add_white_stroke_to_all_icons()
    print(f"\n{'='*50}")
    print(f"Total de SVGs: {total}")
    print(f"Modificados com sucesso: {success}")
