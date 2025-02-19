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
        layout = QtGui.QGridLayout(self)
        label = QtGui.QLabel("Adicionar circuito elétrico", self)
        layout.addWidget(label)


        self.setWindowTitle("Adicionar circuito elétrico ")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.label2 = QtGui.QLabel("Número de fase do circuito elétrico", self)
        layout.addWidget(self.label2)
        
        popupItens1 = ('Trifásico', 'Bifásico', 'Monofásico')
        popup1 = QtGui.QComboBox(self)
        popup1.addItems(popupItens1)
        layout.addWidget(popup1)

        self.label2 = QtGui.QLabel("Método de instalação", self)
        layout.addWidget(self.label2)
        
        popupItens1 = ('A1', 'B2', 'B1', 'B2', 'C', 'D', 'E', 'F', 'G')
        popup1 = QtGui.QComboBox(self)
        popup1.addItems(popupItens1)
        layout.addWidget(popup1)
        
        self.label2 = QtGui.QLabel('Origem', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Destino', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)
        
        self.label2 = QtGui.QLabel('Potência (kW)', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Tensão fase-fase (V)', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Fator de potência', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Potência aparênte (kVA)', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Corrente (A)', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.label2 = QtGui.QLabel('Comprimento do circuito (m)', self)
        layout.addWidget(self.label2)
        self.textInput = QtGui.QLineEdit(self)
        layout.addWidget(self.textInput)

        self.botao = QtGui.QPushButton("Adicionar")
        layout.addWidget(self.botao)
        
        self.botao = QtGui.QPushButton("Cancelar")
        layout.addWidget(self.botao)
        
        self.show()
