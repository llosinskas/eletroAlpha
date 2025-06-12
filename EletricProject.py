import PySide
import os 
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui
import WorkbenchBase
import Sketcher
import Part
import Draft
from utils.create_group import create_group


class ComponentEletric:
    
    def get_point(self):
        point = App.Vector(0,0,0)
        if self.sel and self.sel[0].HasSubObjects:
            point = self.sel[0].PickedPoints[0]
        return point 



    def Activated(self):
        doc=App.activeDocument()
        
        self.sel = Gui.Selection.getSelectionEx()
        point = ComponentEletric.get_point(self)

        # Cria Schetch da simbologia
        sketch_body = doc.addObject('Sketcher::SketchObject', 'Tomada')
        # sketch_body.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0))
        sketch_body.Placement.Base = point 
        
        # Desenha a simbologia
        heigth = 100
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0, 0), App.Vector(heigth/3, 0)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/3, heigth/4), App.Vector(heigth/3, -heigth/4)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/3, heigth/4), App.Vector(heigth, 0)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/3, -heigth/4), App.Vector(heigth, 0)), False)
        sketch_body.addProperty("App::PropertyPower", "potencia")
        
        sketch_body.addProperty("App::PropertyInteger", "Fase")
        sketch_body.addProperty("App::PropertyFloat", "Fator_potencia")
        sketch_body.addProperty("App::PropertyFloat", "altura_piso")
        sketch_body.addProperty("App::PropertyString", "Descricao")
        sketch_body.addProperty("App::PropertyInteger", "Circuito")
        sketch_body.addProperty("App::PropertyElectricPotential", "Tensao")
        sketch_body.addProperty("App::PropertyString", "tipo")
        sketch_body.addProperty("App::PropertyBool", "terra")
        sketch_body.addProperty("App::PropertyBool", "neutro")

        sketch_body.terra = True
        sketch_body.neutro = True
        sketch_body.tipo='tomada'
        sketch_body.Fase = 2
        sketch_body.Fator_potencia = 0.9
        sketch_body.Descricao = "Descrição da tomada"
        sketch_body.potencia =100
        sketch_body.altura_piso = 30
        sketch_body.Circuito = 1
        sketch_body.Tensao = "220"

        doc.recompute()
    def IsActive(self):
        return True
        
    def GetResources(self): 
        return {"Pixmap" :os.path.join(WorkbenchBase.ICON_PATH, 'Componentes.svg'),"MenuText": "Inserir um componente elétrico", "ToolTip":"Inserir um componente no projeto"}
    
class Gerar3D:  
    
    def makeTug(self, tugs, doc):
        
        group = create_group("Equipamentos", doc)
        path_tomadas =""
        if doc.getObject("Tomadas") is not None:
            path_tomadas = doc.getObject("Tomadas")
        else:
            path_tomadas = doc.addObject("App::DocumentObjectGroup", "Tomadas")
        for tug in tugs:

            caixa = doc.addObject('Part::Box', 'tomada')
            caixa.Length = 20
            caixa.Width = 30
            caixa.Height = 30
            posicao = tug.Placement.Base
            Draft.move([caixa], posicao, copy=False)
            Draft.move([caixa], App.Vector(-15,-10,tug.altura_piso), copy=False)
            group.addObject(caixa)
            path_tomadas.addObject(tug)
        
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(doc.Name,"Tomadas")
        Gui.runCommand('Std_ToggleVisibility', 0)
                           

    def Activated(self):
        doc=App.activeDocument()
        list_obj = doc.Objects
        tug = []
        heights = []
        print(list_obj)
        for obj in list_obj:
            if hasattr(obj, 'tipo'):
                if obj.tipo == "tomada":
                    tug.append(obj)
                    heights.append(obj.altura_piso)
        if tug:
            tugs = self.makeTug(tug,doc)
        doc.recompute()

    def GetResources(self):
        return {"Pixmap" : os.path.join(WorkbenchBase.ICON_PATH, "tomadas.svg"), "MenuText" : "Converter em 3D", "ToolTip":"Converter as informações inseridas em modelo 3D"}
    
class Cabo:

    def gerar_2d(self,equipamentos, doc):
        group = create_group("Cabos", doc)
        
        
        for equipamento in equipamentos:
            position = equipamento.Placement.Base
            fase = equipamento.Fase
            neutro = equipamento.neutro
            terra = equipamento.terra
            heigth = 100
            sketch_body = doc.addObject('Sketcher::SketchObject', 'Cabo')
            sketch_body.Placement = App.Placement(position+App.Vector(50,50,0), App.Rotation(0,0,0)) 
            # Terra 
            if terra:
                sketch_body.addGeometry(Part.LineSegment(App.Vector(0, 0), App.Vector(0, heigth/2)), False)
                sketch_body.addGeometry(Part.LineSegment(App.Vector(-heigth/5, heigth/2), App.Vector(0, heigth/2)), False)
            if neutro:
                if terra:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, 0), App.Vector(heigth/2, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2-heigth/5, heigth/2), App.Vector(heigth/2+heigth/5, heigth/2)), False)
                else:
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(0, 0), App.Vector(0, heigth/2)), False)
                    sketch_body.addGeometry(Part.LineSegment(App.Vector(-heigth/5, heigth/2), App.Vector(heigth/5, heigth/2)), False)
            match fase:
                case 1:
                    if neutro and terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                    elif neutro or terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                    else:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                case 2:
                    if neutro and terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                        
                    elif neutro or terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                        
                    else:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                        
                case 3:
                    if neutro and terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth, -heigth/2), App.Vector(heigth+heigth, heigth/2)), False)
                    elif neutro or terra:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth+heigth/2, -heigth/2), App.Vector(heigth+heigth/2, heigth/2)), False)
                    else:
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(0, -heigth/2), App.Vector(0, heigth/2)), False)
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth/2, -heigth/2), App.Vector(heigth/2, heigth/2)), False)    
                        sketch_body.addGeometry(Part.LineSegment(App.Vector(heigth, -heigth/2), App.Vector(heigth, heigth/2)), False)
            group.addObject(sketch_body)
        
    def Activated(self):
        doc=App.activeDocument()
        list_obj = doc.Objects       
        tugs = []
        for obj in list_obj:
            if hasattr(obj, 'tipo'):
                if obj.tipo == "tomada":
                    tugs.append(obj)
                    
        self.gerar_2d(tugs, doc)

        doc.recompute()

    def GetResources(self):
        return {
            "Pixmap" : os.path.join(WorkbenchBase.ICON_PATH, "fio.svg"), 
            "MenuText" : "Gerar cabo", 
            "ToolTip":"Gera a simbologia do cabo em 2D"
        }


Gui.addCommand("ComponentEletric", ComponentEletric())
Gui.addCommand("Gerar3D", Gerar3D())
Gui.addCommand("Cabo", Cabo())