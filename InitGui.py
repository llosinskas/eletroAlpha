"""
Shim de inicialização para a bancada Circuits.
Importa a implementação real do pacote namespace freecad.Circuits.
"""
try:
    import freecad.Circuits.init_gui
except ImportError as e:
    import FreeCAD
    FreeCAD.Console.PrintError(f"Erro ao carregar a bancada Circuits: {e}\n")
