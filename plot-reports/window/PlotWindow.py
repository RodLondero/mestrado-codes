import os, sys
from PyQt5 import QtCore, QtWidgets
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QRect
from numpy import empty    

from functions.functions import plot

class PlotWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.setStyle(QStyleFactory.create("Oxygen"))
        self.setMinimumSize(QSize(440, 120))    
        self.setWindowTitle("Plot Ansys Fluent Reports") 
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_directory = self.base_dir #+ "\\..\\resultados\\"
        self.files = []
        
        for f in os.listdir(self.results_directory):
            if f.endswith(".out"):
                self.files.append(f) 
                     
        centralWidget = QWidget(self, )          
        self.setCentralWidget(centralWidget)   

        self.labelDlg = QLabel(centralWidget)
        self.labelDlg.setGeometry(QRect(40, 10, 180, 30))
        self.labelDlg.setText("Selecione o diretório dos resultados: ")
        
        self.btnOpenFile = QPushButton(centralWidget)
        self.btnOpenFile.setGeometry(QRect(220, 10, 40, 30))
        self.btnOpenFile.setObjectName("btnFileDialog")
        self.btnOpenFile.setText("..")
        self.btnOpenFile.clicked.connect(self.getFolder)
        
        self.label = QLabel(centralWidget)
        self.label.setGeometry(QRect(40, 50, 300, 31))
        self.label.setObjectName("labelCombo")
        self.label.setText("Escolha um gráfico para plotar:")
        
        # Create combobox and add items.
        self.comboBox = QComboBox(centralWidget)
        self.comboBox.setGeometry(QRect(40, 80, 300, 31))
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.clear()        
        
        for f in self.files:
            self.comboBox.addItem(f)
            
        self.button = QPushButton(centralWidget)
        self.button.setGeometry(QRect(340, 80, 60, 31))
        self.button.setText("Plotar")
        self.button.clicked.connect(self.click)

    def click(self):
        try:
            if self.comboBox.currentText() == "":
                raise Exception("Selecione um arquivo para plotar")
            
            plot(self.results_directory + self.comboBox.currentText())
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro")
            msg.setInformativeText("{0}".format(e))
            msg.setWindowTitle("Erro")
            msg.exec_()
        
    def getFolder(self):
        fname = QFileDialog.getExistingDirectory(self, "Selecione o diretório.")
        
        if fname != "":
            self.results_directory = fname + "/"
            
            self.files = []
            for f in os.listdir(fname):
                if f.endswith(".out"):
                    self.files.append(f)        
        
            self.comboBox.clear()        
            for f in self.files:
                self.comboBox.addItem(f)