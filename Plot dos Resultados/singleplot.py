import sys, os
from PyQt5 import QtCore, QtWidgets
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QRect    
import math

from matplotlib.ticker import (MultipleLocator)
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class PlotWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.setStyle(QStyleFactory.create("Oxygen"))
        self.setMinimumSize(QSize(440, 120))    
        self.setWindowTitle("Combobox example") 
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_directory = self.base_dir + "\\resultados\\"
        self.files = []
        for f in os.listdir(self.results_directory):
            if f.endswith(".out"):
                self.files.append(f) 
                     
        centralWidget = QWidget(self)          
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
        plot(self.results_directory + self.comboBox.currentText())
        
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
        
def plot(file_name: str):
    fig = plt.figure(figsize=(9, 5))  # type: figure.Figure
    ax = plt.subplot()
    
    df = read_file(file_name)
    df['flow-time'] = df['flow-time'] * 1000
    
    for v in df.copy():
        if v != 'flow-time':
            df[v] = df[v].round(2)

    ax = df.plot(x='flow-time', ax=ax,
                 title=df.name,
                 xlabel='Tempo ($ms$)',
                #  xlim=(0, round_up(max(df['flow-time']), -1)),
                #  ylim=ylim,
                 label=df.name)

    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)
    # ax.xaxis.set_major_locator(MultipleLocator(10))
    # ax.xaxis.set_minor_locator(MultipleLocator(5))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=True, ncol=5)

    # fig.tight_layout()
    # fig.subplots_adjust(hspace=0.3)
    # plt.get_current_fig_manager().window.showMaximized()
    plt.show()

def read_file(filename: str):
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
    dataframe = dataframe.set_index('Time Step')
    dataframe.name = title

    return dataframe


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = PlotWindow()
    mainWin.show()
    sys.exit( app.exec_() )