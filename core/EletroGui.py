# 
# Author: Lucas Losinskas
# date: 08/2023
# Criar as telas de adicionar elementos, circuitos.

from PySide import QtCore, QtGui
import FreeCAD as App
import FreeCADGui as Gui 


class MainDialog(QtGui.QDialog):
    def __init__(self):
    
        super(MainDialog, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(QtCore.QRect(100, 100, 500, 500) )
        self.setWindowTitle("Adicionar circuito elétrico")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.label2 = QtGui.QLabel("Número de fase do circuito", self)
        self.label2.move(5, 30)
        
        self.popupItens1 = ('Trifásico', 'Bifásico', 'Monofásico')
        self.popup1 = QtGui.QComboBox(self)
        self.popup1.addItems(self.popupItens1)
        self.popup1.move(200, 30)

        self.label2 = QtGui.QLabel("Método de instalação", self)
        self.label2.move(5, 50)
        
        self.popupItens1 = ('A1', 'B2', 'B1', 'B2', 'C', 'D', 'E', 'F', 'G')
        self.popup1 = QtGui.QComboBox(self)
        self.popup1.addItems(self.popupItens1)
        self.popup1.move(200, 50)
        
        self.label2 = QtGui.QLabel('Origem', self)
        self.label2.move(5, 70)
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.move(200, 70)

        self.label2 = QtGui.QLabel('Destino', self)
        self.label2.move(5, 90)
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.move(200, 90)

        self.label2 = QtGui.QLabel('Potência (kW)', self)
        self.label2.move(5, 110)
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.move(200,110)

        self.label2 = QtGui.QLabel('Tensão fase-fase (V)', self)
        self.label2.move(5, 130)
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.move(200, 130)

        self.label2 = QtGui.QLabel('Fator de potência', self)
        self.label2.move(5, 150)
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.move(200, 150)


        pushButton1 = QtGui.QPushButton('Adicionar', self)
        pushButton1.move(200, 400)

        pushButton1 = QtGui.QPushButton('Cancelar', self)
        pushButton1.move(300, 400)

        self.show()
