import sys, os, pathlib, math
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import pandas as pd

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.ticker import (MultipleLocator)

from .calculos import Executar
from .energia_incidente_astm import calc_by_ASTM

pathdir = pathlib.Path(__file__).parent.absolute()

class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/window.ui', self) 
        
        self.initUI()
            
    def initUI(self):
        self.setWindowTitle("Calculo de Energia Incidente")
        self.setMinimumSize(425, 300)
        self.setFixedSize(425, 300)
        
        self.getComponents()
        self.setCommands()
                    
        self.show()
        
    def getComponents(self):    
        self.lineEdit        = self.findChild(QLineEdit,   'lineEdit')        # type: QLineEdit
        self.btnFile         = self.findChild(QToolButton, 'toolButton')      # type: QToolButton
        self.btnCalcular     = self.findChild(QPushButton, 'btnCalcular')     # type: QToolButton
        self.btnAbrir        = self.findChild(QPushButton, 'btnAbrir')        # type: QToolButton
        self.comboBoxSep     = self.findChild(QComboBox,   'comboBoxSep')     # type: QComboBox
        self.comboBoxDecimal = self.findChild(QComboBox,   'comboBoxDecimal') # type: QComboBox
        self.checkBoxHTML    = self.findChild(QCheckBox,   'checkBoxHTML')    # type: QCheckBox
        self.checkBoxCSV     = self.findChild(QCheckBox,   'checkBoxCSV')     # type: QCheckBox       
        self.checkBoxPDF     = self.findChild(QCheckBox,   'checkBoxPDF')     # type: QCheckBox
        self.checkBoxSVG     = self.findChild(QCheckBox,   'checkBoxSVG')     # type: QCheckBox
        self.list1           = self.findChild(QListWidget, 'listWidget')      # type: QListWidget

    def setCommands(self):
        self.btnFile.clicked.connect(self.openFileNameDialog)
        self.btnCalcular.clicked.connect(self.calcular_ei)
        self.btnAbrir.clicked.connect(self.abrirArquivos)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            self.lineEdit.setText(fileName)
    
    def calcular_ei(self):
        try:
            if self.lineEdit.text() == "":
                raise Exception("Selecione um arquivo.")

            if not self.list1.selectedItems():
                raise Exception("Selecione uma coluna")

            path      = self.lineEdit.text()
            separador = " " if str(self.comboBoxSep.currentText()) == "Espaço" else str(self.comboBoxSep.currentText()) 
            decimal   = str(self.comboBoxDecimal.currentText())
            
            calc_by_ASTM(self.df, self.list1.selectedItems()[0].text())
            
            # result = Executar(self.df.copy())
            max_EI = f"{self.df['EI'].max():.4f} [cal/cm^2]"

            print(f"\nMáxima EI: {max_EI}")

            self.fig = plt.figure(figsize=(10, 5))    # type: figure.Figure
            self.ax = self.fig.subplots(1, 2)    # type: axes.Axes

            self.plot(ax=self.ax[0],
                      column=self.df.columns[1],
                      title="Temperatura",
                      xlabel='Tempo ($ms$)',
                      ylabel='Temperatura ($K$)')

            self.plot(ax=self.ax[1],
                      column='EI',
                      title="Energia Incidente",
                      xlabel='Tempo ($ms$)',
                      ylabel='Energia Incidente ($cal/cm^2$)')

            self.fig.tight_layout()
            # self.fig.subplots_adjust(hspace=0.3)
            # plt.get_current_fig_manager().window.showMaximized()
            plt.show()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Máxima EI")
            msg.setInformativeText(max_EI)
            msg.setWindowTitle("Informação")
            msg.exec_()
        except Exception as e:
            print("{0}".format(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro")
            msg.setInformativeText("{0}".format(e))
            msg.setWindowTitle("Erro")
            msg.exec_()
    
    def abrirArquivos(self):
        try:
            fileName = self.lineEdit.text()

            if fileName == "":
                raise Exception("Selecione um arquivo para abrir")

            self.getFileColumns(path=fileName)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro")
            msg.setInformativeText("{0}".format(e))
            msg.setWindowTitle("Erro")
            msg.exec_()

    def getFileColumns(self, path: str):

        separador = " " if str(self.comboBoxSep.currentText()) == "Espaço" else str(self.comboBoxSep.currentText()) 
        decimal   = str(self.comboBoxDecimal.currentText())

        _, file_extension = os.path.splitext(path)

        if file_extension == ".csv":
            self.df = pd.read_csv(path, sep=separador, decimal=decimal)   # type: pd.DataFrame
        elif file_extension == ".out":
            self.df = self.readOutFile(path)

        self.list1.clear()

        for c in self.df.columns:
            if c.lower().strip().replace(" ", "-") not in ['time-step', 'flow-time']:
                self.list1.addItem(c)

    def readOutFile(self, filename: str):

        with open(filename, 'r') as f:
            content = f.read().splitlines()

            # Get title
            title = content[0].strip('"')

            # Remove the second line of the file
            content.pop(1)

            # Get columns
            columns = content[1].strip("()\n").split('"')
            for i, val in enumerate(columns):
                if val.strip() == '':
                    columns.pop(i)

            # Format values to Float
            for i in range(0, len(content[2:])):
                line = content[2:][i].strip('\n').split(' ')
                line = [float(item) for item in line]

                content[i + 2] = line

        dataframe = pd.DataFrame(content[2:], columns=columns)
        # dataframe = dataframe.set_index('Time Step')
        dataframe.name = title

        return dataframe

    def plot(self, ax: axes.Axes, column: str, **kwargs):

        df = self.df.copy()

        df['flow-time'] = df['flow-time'] * 1000

        x = df['flow-time']
        y = df[column]

        title  = kwargs['title']  if 'title'  in kwargs else None
        label  = kwargs['label']  if 'label'  in kwargs else None
        xlabel = kwargs['xlabel'] if 'xlabel' in kwargs else 'Tempo (s)'
        ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Amplitude'

        min_x = 0
        max_x = max(x)
        delta_x = round_up(max_x - min_x)
        major_ticks_x = delta_x / 10
        minor_ticks_x = delta_x / 10 / 2

        min_y = round(min(y))
        max_y = max(y)
        delta_y = round_up(max_y - min_y)
        major_ticks_y = delta_y / 10
        minor_ticks_y = delta_y / 10 / 2

        ax = df.plot(x='flow-time', y=column, ax=ax, style='o-',
                     title=title,
                     label=label,
                     xlabel=xlabel,
                     ylabel=ylabel,
                     xlim=(0, round_up(max_x,-1)),
                     ylim=(min_y, max_y+major_ticks_y)
        )

        ax.xaxis.set_major_locator(MultipleLocator(major_ticks_x))
        ax.xaxis.set_minor_locator(MultipleLocator(minor_ticks_x))

        ax.yaxis.set_major_locator(MultipleLocator(major_ticks_y))
        ax.yaxis.set_minor_locator(MultipleLocator(minor_ticks_y))

        ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
        ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)

    def get_max_EI(self):
        return self.df['EI'].max()

    def read_file(self):
        _, file_extension = os.path.splitext(self.file_path)

        if file_extension == ".csv":
            self.df = pd.read_csv(self.file_path, sep=self.csv_sep, decimal=self.csv_decimal)   # type: pd.DataFrame
        elif file_extension == ".out":
            self.df = self.readOutFile(self.file_path)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier