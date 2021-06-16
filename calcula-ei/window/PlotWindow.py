import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
            
    def initUI(self):
        self.setWindowTitle("Calculo de Energia Incidente")
        self.setMinimumSize(QSize(400, 60))    
        self.setFixedSize(400, 32*3)
        
        self.createGridLayout()
                    
        self.show()
        
    def createGridLayout(self):
        self.windowLayout = QGridLayout()

        self.label1 = QLabel("Selecione o arquivo de temperaturas")
        
        self.editFileSelect = QTextEdit()
        
        self.btnFileSelect = QPushButton('...')
        self.btnFileSelect.clicked.connect(self.openFileNameDialog)
        
        self.btnCalcularEI = QPushButton('Calcular EI')
        self.btnCalcularEI.clicked.connect(self.actionClickCalcularEI)
        
        self.windowLayout.addWidget(self.label1, 0, 0)
        self.windowLayout.addWidget(self.editFileSelect, 1, 0,)
        self.windowLayout.addWidget(self.btnFileSelect, 1, 1)
        self.windowLayout.addWidget(self.btnCalcularEI, 2, 0, 1, 2)
        
        self.setLayout(self.windowLayout)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            self.editFileSelect.setText(fileName)
    
    def actionClickCalcularEI(self):
        if self.editFileSelect.toPlainText() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Atenção")
            msg.setInformativeText("Selecione um arquivo.")
            msg.setWindowTitle("Atenção")
            msg.exec_()
        else:
            pass