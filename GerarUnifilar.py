

# Gerar o diagrama unifilar

import os
import FreeCADGui as Gui
import FreeCAD as App
import WorkbenchBase as WB
import Part 
import Draft

class GerarUnifilar:
    def gerar_linha(self,doc, potencia, dr, bitola, position, corrente, comprimento):
        sketch_body = doc.addObject("Sketcher::SketchObject", "Diagrama unifilar simples")
        sketch_body.Placement = position
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0,-comprimento/2),App.Vector(0, comprimento/2)), False)
        sketch_body.addGeometry(Part.LineSegment(App.Vector(0,0),App.Vector(comprimento/2,0) ), False)
        if dr:
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,-comprimento/2), App.Vector(comprimento,-comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,-comprimento/2), App.Vector(comprimento/2,comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2,comprimento/2), App.Vector(comprimento,comprimento/2)), False)
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento,-comprimento/2), App.Vector(comprimento,comprimento/2)), False)
            
            center_position = App.Vector(comprimento,comprimento)
            text = Draft.make_text(["DR"], placement =center_position , screen =None, height=None, line_spacing=None)
            print(text.Label)
            text.Label= "DR"
            Draft.autogroup(text)
        else:
            sketch_body.addGeometry(Part.LineSegment(App.Vector(comprimento/2, 0), App.Vector(comprimento, 0)), False)


        text = Draft.make_text([f"{potencia}"], placement = position, screen =None, height=None, line_spacing=None)
        Draft.autogroup(text)


    def Activated(self):
        doc = App.activeDocument()
        position = App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0))
        heigth =100
        GerarUnifilar.gerar_linha(self, doc, 100,True, 2.5,position, 30, heigth)




        doc.recompute()
    def IsActive(self):
        return True
    
    def GetResources(self):
        # return {'Pixmap' : WB.IMAGE_PATH/"tomadas.svg", 'MenuText': "Gerar diagrama unifilar", "Tooltip":"Gerar um diagrama unifilar a partir dos dados inseridos no projeto"}
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'unifilar.svg'), 'MenuText':'Gerar unifilar', 'ToolTip':'Gerar diagrama unifilar dos quadros do projeto'}


Gui.addCommand("GerarUnifilar", GerarUnifilar())