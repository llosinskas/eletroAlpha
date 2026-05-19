import FreeCAD as App
import Part
import FreeCADGui as Gui

class ConduitPath:
    """FeaturePython customizado para representar o caminho 2D de um Eletroduto."""
    
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ConduitPath"
        self._add_properties(obj)
        
    def _add_properties(self, obj):
        # Pontos do traçado (no plano Z=0)
        obj.addProperty("App::PropertyVectorList", "Points", "Conduit", "Pontos do caminho no plano base").Points = []
        
        # Propriedades para a geração 3D
        obj.addProperty("App::PropertyDistance", "Altura3D", "Conduit", "Altura do eletroduto no 3D").Altura3D = 2800.0
        
        # Diâmetros nominais (usando Enumeration)
        obj.addProperty("App::PropertyEnumeration", "Diametro", "Conduit", "Tamanho nominal do eletroduto")
        obj.Diametro = ["1/2", "3/4", "1", "1 1/4", "1 1/2", "2", "3", "4"]
        obj.Diametro = "3/4"
        
        # Tipo do eletroduto
        obj.addProperty("App::PropertyEnumeration", "Tipo", "Conduit", "Flexível (Curvas suaves) ou Rígido (Ângulos retos)")
        obj.Tipo = ["Flexível", "Rígido"]
        obj.Tipo = "Flexível"

    def execute(self, obj):
        points = obj.Points
        if not points or len(points) < 2:
            return
        
        # Cria a geometria 2D estritamente no plano Z=0
        edges = []
        for i in range(len(points) - 1):
            p1 = App.Vector(points[i].x, points[i].y, 0)
            p2 = App.Vector(points[i+1].x, points[i+1].y, 0)
            
            # Evita linhas de tamanho zero
            if (p2 - p1).Length > 1e-5:
                edges.append(Part.makeLine(p1, p2))
            
        if edges:
            wire = Part.Wire(edges)
            obj.Shape = wire
            
    def onChanged(self, fp, prop):
        if prop in ["Points"]:
            pass # FreeCAD auto-calls execute when properties change
            
class ViewProviderConduitPath:
    """Provedor visual para o ConduitPath."""
    
    def __init__(self, vobj):
        vobj.Proxy = self
        
    def getIcon(self):
        import os
        from freecad.Circuits import ICON_PATH
        return os.path.join(ICON_PATH, "conduite.svg")
        
    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        
    def updateData(self, fp, prop):
        pass
        
    def onChanged(self, vp, prop):
        pass
        
    def getDefaultDisplayMode(self):
        return "Flat Lines"

def create_conduit_path(name="ConduitPath", points=None):
    """Função utilitária para criar e configurar um ConduitPath no documento ativo."""
    doc = App.activeDocument()
    if not doc:
        return None
        
    obj = doc.addObject("Part::FeaturePython", name)
    ConduitPath(obj)
    ViewProviderConduitPath(obj.ViewObject)
    
    if points:
        obj.Points = points
        
    doc.recompute()
    return obj
