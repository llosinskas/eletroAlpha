"""
__author__ = "llosinskas"
__copyright__ = "2025 llosinskas"
__reference__ = "Kliurka"
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtWidgets
import Part
import Draft
import xml.etree.ElementTree as ET
import csv
import os 


class ImportQET:
    def import_qet(doc):
        input_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Selecione o Arquivo do QEletrotech .qet", "", "Arquivo QET (*.qet)")
        if not input_file:
            print("Sem arquivo selecionado")
            return
        try: 
            tree = ET.parse(input_file)
            root = tree.getroot()
        except ET.ParseError as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Erro ao abrir o arquivo QET: {str(e)}")
            return
        
        conductors = root.findall(".//conductor")
        if not conductors:
            QtWidgets.QMessageBox.warning(None, "Warning", "Não há dados de cabos dentro do arquivo do QEletrotech.")
            return 
        
        file_name= os.path.splitext(os.path.basename(input_file))[0]
        spreadsheet = doc.addObject("Spreadsheet::Sheet", file_name)
        spreadsheet.Label = file_name

        # Escrever o cabeçalho da tabela
        spreadsheet.set("A1", "Wire ID")
        spreadsheet.set("B1", "From Ref")
        spreadsheet.set("C1", "From Pin")
        spreadsheet.set("D1", "To Ref")
        spreadsheet.set("E1", "To Pin")
        spreadsheet.set("F1", "Area")
        spreadsheet.set("G1", "Color")
        spreadsheet.set("H1", "Wire Length")
        spreadsheet.set("I1", "Unique Code")
        spreadsheet.set("J1", "Cable")

        wire_connections = {}
        regular_wires = []

        for conductor in conductors:
            wire_id = conductor.get("num", "")
            element1_name = conductor.get("element1_name", "")
            element2_name = conductor.get("element2_name", "")
            conductor_color = conductor.get("conductor_color", "")
            conductor_section = conductor.get("conductor_section", "")

            if wire_id not in wire_connections:
                wire_connections[wire_id] = {
                    "color": conductor_color, 
                    "section": conductor_section, 
                    "from_ref": None, 
                    "from_pin": None, 
                    "to_ref": None, 
                    "to_pin": None, 
                }

            if element1_name == "Going arrow":
                wire_connections[wire_id]["from_ref"] = conductor.get("element2_label", "")
                wire_connections[wire_id]["from_pin"] = conductor.get("terminalname2", "") 
            elif element2_name == "Going arrow":
                wire_connections[wire_id]["from_ref"] = conductor.get("element1_label", "")
                wire_connections[wire_id]["from_pin"] = conductor.get("terminalname1", "")
            if element1_name == "Coming arrow":
                wire_connections[wire_id]["to_ref"] = conductor.get("element2_label", "")
                wire_connections[wire_id]["to_pin"] = conductor.get("terminalname2", "")
            elif element2_name == "Coming arrow":
                wire_connections[wire_id]["to_ref"] = conductor.get("element1_label", "")
                wire_connections[wire_id]["to_pin"] = conductor.get("terminalname1", "")

            if element1_name != "Going arrow" and element1_name != "Coming arrow" and element2_name != "Going arrow" and element2_name != "Coming arrow":
                element1_linked = conductor.get("element1_linked", "")
                if element1_linked:
                    from_ref = element1_linked
                else:
                    from_ref = conductor.get("element1_label", "")
                from_pin = conductor.get("terminalname1", "")
            
                element2_linked = conductor.get("element2_linked", "")
                if element2_linked:
                    to_ref = element2_linked
                else:
                    to_ref = conductor.get("element2_label", "")
                
                to_pin = conductor.get("terminalname2", "")

                regular_wires.append({
                    "wire_id": wire_id, 
                    "from_ref":from_ref, 
                    "from_pin":from_pin, 
                    "to_ref": to_ref, 
                    "to_pin":to_pin, 
                    "section": conductor_section,
                    "color": conductor_color, 
                })
        row = 2
        for wire in regular_wires:
            spreadsheet.set(f"A{row}", wire["wire_id"])
            spreadsheet.set(f"B{row}", wire["from_ref"])
            spreadsheet.set(f"C{row}", wire["from_pin"])
            spreadsheet.set(f"D{row}", wire["to_ref"])
            spreadsheet.set(f"E{row}", wire["to_pin"])
            spreadsheet.set(f"F{row}", wire["section"])
            spreadsheet.set(f"G{row}", wire["color"])
            row += 1

        for wire_id, connection in wire_connections.items():
            if connection["from_ref"] and connection["to_ref"]:
                spreadsheet.set(f"A{row}", wire_id)
                spreadsheet.set(f"B{row}", connection["from_ref"])
                spreadsheet.set(f"C{row}", connection["from_pin"])
                spreadsheet.set(f"D{row}", connection["to_ref"])
                spreadsheet.set(f"E{row}", connection["to_pin"])
                spreadsheet.set(f"F{row}", connection["section"])
                spreadsheet.set(f"G{row}", connection["color"])
                row += 1

    def check_duplicate_labels():
        duplicate_labels = App.ParamGet("User parameter:BaseApp/Preferences/Document").GetBool("DuplicateLabels")

        if duplicate_labels:
            print("DuplicateLabels is OK ")
            return True
        else: 
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("Elementos duplicados")
            dialog.setText("Para o funcionamento correto só pode existir um elemento com o Label no documento.")
            dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
            dialog.button(QtWidgets.QMessageBox.Yes).setText("Allow")
            dialog.button(QtWidgets.QMessageBox.Cancel).setText("Cancel")

            result = dialog.exec_()

            if result == QtWidgets.QMessageBox.Yes:
                App.ParamGet("User parameter:BaseApp/Preferences/Document").SetBool("DuplicateLabels", True)
                print("DuplicateLabels has been enabled.")
                return True
            else: 
                print("Execução do Script cancelada por usuário.")
                return False
        
    def find_object_by_label(doc, label):
        if hasattr(doc, "Objects"):
            for obj in doc.Objects:
                if obj.Label == label:
                    return obj
                if hasattr(obj, "Group"):
                    for sub_obj in obj.Group:
                        if sub_obj.Label == label:
                            return sub_obj
        elif hasattr(doc, "Group"):
            for obj in doc.Group:
                if obj.Label == label:
                    return obj
        return None

    def Activated(self):
        doc = App.activeDocument()
        if not doc:
            doc = App.newDocument()
        ImportQET.import_qet(doc)    
        ImportQET.check_duplicate_labels()
        doc.recompute()
        

        # doc.recompute()
    def IsActive(self):
        return True
    
    def GetResources(self):
        
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'QET-logo.png'), 'MenuText':'Importar .qet', 'ToolTip':'Importar um arquivo do QEletroTech para a geração de componentes 3D e cabos'}

class Add_Node:
    def AddNo(doc):
        selection = Gui.Selection.getSelection()
        if not selection:
            print("Linha não selecionada!")
            return 
        
        selected_object = selection[0]
        if not hasattr(selected_object, "Points"):
            print("Objeto selecionado não é possível inserir um ponto")
            return 
        
        if len(selected_object.Points) <2:
            print("Não é posssível adicionar um ponto de controle!")
            return 
        new_points = []
        for i in range(len(selected_object.Points)-1):
            new_points.append(selected_object.Points[i])
            mid_points = (selected_object.Points[i]+selected_object.Points[i+1])*0.5
            new_points.append(mid_points)

        new_points.append(selected_object.Points[-1])
        selected_object.Points = new_points
        selected_object.touch()
        doc.recompute()
        print(f"Adicionado pontos de controle na curva: {selected_object.Label}")

    def Activated(self):
        doc = App.activeDocument()
        Add_Node.AddNo(doc)
    def IsActive(self):
        return True
    
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'Draft_AddPoint.svg'), 'MenuText':'Adicionar ponto', 'ToolTip':'Adicionar um ponto na linha para edição do caminho dos cabos'}

class Create_connection:
    def get_values_from_table():
        mw = Gui.getMainWindow()
        view = mw.getActiveWindow()
        if view and hasattr(view, "selectedCells"):
            selected_cell = view.selectedCells()

    def create_connection(doc):
        if not doc:
            print("Sem arquivo ativo")
            return 
        value = Create_connection.get_values_from_table()

    def Activated(self):
        doc = App.activeDocument()
        Create_connection.create_connection(doc)
    
    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources/Icons", 'Draft_AddPoint.svg'), 'MenuText':'Adicionar ponto', 'ToolTip':'Adicionar um ponto na linha para edição do caminho dos cabos'}



Gui.addCommand("ImportQET", ImportQET())
Gui.addCommand("Add_Node", Add_Node())