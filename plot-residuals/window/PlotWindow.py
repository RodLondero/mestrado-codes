import os
import sys
from PyQt5 import QtCore, QtWidgets
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QRect
from numpy import empty

from functions.plot import main

class PlotWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.setStyle(QStyleFactory.create("Oxygen"))
        self.setMinimumSize(QSize(440, 160))
        self.setWindowTitle("Plot Ansys Fluent Reports")
       
        self.results_directory = os.path.dirname(os.path.abspath(__file__))
        self.results_directory = ".\\"
        
        self.files = []
        self.file_extension = ".trn"

        for f in os.listdir(self.results_directory):
            if f.endswith(self.file_extension):
                self.files.append(f)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.labelDlg = QLabel(self.centralWidget)
        self.labelDlg.setGeometry(QRect(40, 10, 220, 30))
        self.labelDlg.setText("Selecione o diretório dos resultados: ")

        self.btnOpenFile = QPushButton(self.centralWidget)
        self.btnOpenFile.setGeometry(QRect(250, 10, 40, 30))
        self.btnOpenFile.setObjectName("btnFileDialog")
        self.btnOpenFile.setText("..")
        self.btnOpenFile.clicked.connect(self.getFolder)

        self.label = QLabel(self.centralWidget)
        self.label.setGeometry(QRect(40, 50, 300, 31))
        self.label.setObjectName("labelCombo")
        self.label.setText("Escolha um gráfico para plotar:")

        # Create combobox and add items.
        self.comboBox = QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QRect(40, 80, 300, 31))
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.clear()

        for f in self.files:
            self.comboBox.addItem(f)

        self.button = QPushButton(self.centralWidget)
        self.button.setGeometry(QRect(340, 80, 60, 31))
        self.button.setText("Plotar")
        self.button.clicked.connect(self.click)

        self.checkBoxSalvarHTML = QCheckBox(self.centralWidget)
        self.checkBoxSalvarHTML.setGeometry(QRect(40, 120, 100, 30))
        self.checkBoxSalvarHTML.setText("Salvar HTML")
        self.checkBoxSalvarHTML.stateChanged.connect(self.checkBoxChangeAction)
        
        self.checkBoxSalvarCSV = QCheckBox(self.centralWidget)
        self.checkBoxSalvarCSV.setGeometry(QRect(150, 120, 90, 30))
        self.checkBoxSalvarCSV.setText("Salvar CSV")
        self.checkBoxSalvarCSV.stateChanged.connect(self.checkBoxChangeAction)
        
        self.labelSaveFile = QLabel(self.centralWidget)
        self.labelSaveFile.setGeometry(QRect(40, 150, 220, 30))
        self.labelSaveFile.setText("Selecione o diretório para salvar os arquivos: ")
        self.labelSaveFile.hide()
        
        self.textPathtoSave = QTextEdit(self.centralWidget)
        self.textPathtoSave.setGeometry(QRect(40, 180, 340, 30))
        self.textPathtoSave.setObjectName("editPathtoSave")
        
        self.btnOpenFiletoSave = QPushButton(self.centralWidget)
        self.btnOpenFiletoSave.setGeometry(QRect(380, 180, 40, 30))
        self.btnOpenFiletoSave.setObjectName("btnOpenFiletoSave")
        self.btnOpenFiletoSave.setText("..")
        self.btnOpenFiletoSave.clicked.connect(self.getFoldertoSave)
        self.btnOpenFiletoSave.hide()       
        

    def click(self):
        try:
            if self.comboBox.currentText() == "":
                raise Exception("Selecione um arquivo para plotar")

            main(self.results_directory, self.comboBox.currentText(),
                 salvar_html=self.checkBoxSalvarHTML.isChecked,
                 salvar_csv=self.checkBoxSalvarCSV.isChecked,
                 path_to_save=self.textPathtoSave.toPlainText())
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro")
            msg.setInformativeText("{0}".format(e))
            msg.setWindowTitle("Erro")
            msg.exec_()

    def getFolder(self):
        fname = QFileDialog.getExistingDirectory(
            self, "Selecione o diretório.")

        if fname != "":
            self.results_directory = fname + "/"

            self.files = []
            for f in os.listdir(fname):
                if f.endswith(self.file_extension):
                    self.files.append(f)

            self.comboBox.clear()
            for f in self.files:
                self.comboBox.addItem(f)

    def checkBoxChangeAction(self):        
        if self.checkBoxSalvarHTML.isChecked() or self.checkBoxSalvarCSV.isChecked():
            self.labelSaveFile.show()
            self.btnOpenFiletoSave.show()
            self.setMinimumSize(QSize(440, 220))
            self.resize(QSize(440, 220))
        else:
            self.labelSaveFile.hide()
            self.btnOpenFiletoSave.hide()
            self.textPathtoSave.clear()
            self.setMinimumSize(QSize(440, 160))
            self.resize(QSize(440, 160))
            
    def getFoldertoSave(self):
        fname = QFileDialog.getExistingDirectory(
            self, "Selecione o diretório.")

        if fname != "":
            self.textPathtoSave.setText(fname)