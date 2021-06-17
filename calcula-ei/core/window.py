import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from .calculos import Executar

class App(QWidget):

    def __init__(self, csv_sep: str = ";", csv_decimal: str = ","):
        super().__init__()
        
        self.csv_sep = csv_sep
        self.csv_decimal = csv_decimal

        self.initUI()
            
    def initUI(self):
        self.setWindowTitle("Calculo de Energia Incidente")
        self.setMinimumSize(QSize(400, 60))    
        self.setFixedSize(400, 36*3)
        
        self.createGridLayout()
                    
        self.show()
        
    def createGridLayout(self):
        self.windowLayout = QGridLayout()

        self.label1 = QLabel("Selecione o arquivo de temperaturas (.csv)")
        
        self.editFileSelect = QLineEdit()
        
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
        if self.editFileSelect.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Atenção")
            msg.setInformativeText("Selecione um arquivo.")
            msg.setWindowTitle("Atenção")
            msg.exec_()
        else:
            try:
                result = Executar(file_path=self.editFileSelect.text(), csv_sep=self.csv_sep, csv_decimal=self.csv_decimal)
                max_EI = f"{result.get_max_EI():.4f} [cal/cm^2]"

                print(f"\nMáxima EI: {max_EI}")

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Máxima EI")
                msg.setInformativeText(max_EI)
                msg.setWindowTitle("Informação")
                msg.exec_()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Erro")
                msg.setInformativeText("{0}".format(e))
                msg.setWindowTitle("Erro")
                msg.exec_()

