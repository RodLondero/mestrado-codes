from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, datetime
import numpy as np

import pandas as pd
import sys, os, csv
import plotly.express as px
import plotly.graph_objs as go
import pathlib


pathdir = pathlib.Path(__file__).parent.absolute()

symbols = ['circle', 'square', 'triangle-up', 'cross', 'star']
dash = ["solid", "dot", "dash", "dashdot", "longdash", "longdashdot"]

class Ui(QMainWindow):
    def __init__(self, root_path: str = None):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/window.ui', self)  # Load the .ui file
        
        self.setFixedSize(550, 380)
        
        self.__findElements()
        
        self.dfs = list()
        self.columns = list()
        self.editPasta.setText(root_path)
        self.loadFiles(root_path)
        
        self.show()
        
    def __findElements(self):
        # Edits
        self.editPasta  = self.findChild(QLineEdit, 'editPasta')  # type: QLineEdit

        # Lists
        self.listArquivos = self.findChild(QListWidget, 'listArquivos')     # type: QListWidget
        self.listArquivos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listArquivos.itemSelectionChanged.connect(self.clickAbrir)
        
        self.listColunas = self.findChild(QListWidget, 'listColunas')       # type: QListWidget
        self.listColunas.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Buttons
        self.btnPasta  = self.findChild(QToolButton, 'btnPasta')    # type: QToolButton
        self.btnPasta.clicked.connect(self.openFolderDialog)
        
        self.btnAbrir  = self.findChild(QPushButton, 'btnAbrir')    # type: QPushButton
        self.btnAbrir.clicked.connect(self.clickAbrir)
        self.btnPlotar = self.findChild(QPushButton, 'btnPlotar')   # type: QPushButton
        self.btnPlotar.clicked.connect(self.clickPlotar)
        self.btnAtualizar = self.findChild(QPushButton, 'btnAtualizar')   # type: QPushButton
        self.btnAtualizar.clicked.connect(self.clickAtualizar)

        # ComboBox
        self.comboSep     = self.findChild(QComboBox, 'comboSep')       # type: QComboBox
        self.comboSep.currentTextChanged.connect(self.clickAbrir)
        self.comboDecimal = self.findChild(QComboBox, 'comboDecimal')   # type: QComboBox
        self.comboDecimal.currentTextChanged.connect(self.clickAbrir)
        
        # CheckBox
        self.checkBoxHTML = self.findChild(QCheckBox, 'checkBoxHTML') # type: QCheckBox
        self.checkBoxCSV  = self.findChild(QCheckBox, 'checkBoxCSV')  # type: QCheckBox       
        self.checkBoxPDF  = self.findChild(QCheckBox, 'checkBoxPDF')  # type: QCheckBox
        self.checkBoxSVG  = self.findChild(QCheckBox, 'checkBoxSVG')  # type: QCheckBox
        
        
    def openFolderDialog(self):
        fname = QFileDialog.getExistingDirectory(self, "Selecione o diretório.")
        if fname != "":
            self.editPasta.setText(fname + "/")
            self.loadFiles(fname)
            
    def loadFiles(self, fname):
        self.listArquivos.clear()
        for f in os.listdir(fname):
            if f.endswith(".out") or f.endswith('.csv'):
                self.listArquivos.addItem(f)
                    
    def clickAtualizar(self):
        try:
            if self.editPasta.text() == "":
                raise Exception("Selecione uma pasta.")
            
            self.loadFiles(self.editPasta.text())
            
        except Exception as e:
            mensagemErro(e)
    
    def clickPlotar(self):
        try:
            if not self.listColunas.selectedItems():
                raise Exception("Selecione uma coluna para plotar")
            
            self.plotar()
        except Exception as e:
            mensagemErro(e)
            
    def clickAbrir(self):
        try:
            if self.editPasta.text() == "":
                raise Exception("Selecione um arquivo para abrir")
            
            self.dfs.clear()
            self.listColunas.clear()
            self.columns.clear()
                        
            for arquivo in self.listArquivos.selectedItems():
                path = os.path.join(self.editPasta.text(), arquivo.text())
                self.getFileColumns(path)
                
            self.listColunas.addItems(self.columns)
                        
        except Exception as e:
            mensagemErro(e)
    
    def getFileColumns(self, path: str):

        file_path, file_extension = os.path.splitext(path)
        name = file_path.replace("/", "\\").split("\\")[-1]

        if file_extension == ".csv":
            separador = " " if str(self.comboSep.currentText()) == "Espaço" else str(self.comboSep.currentText()) 
            decimal = str(self.comboDecimal.currentText())
            
            df = pd.read_csv(path, sep=separador, decimal=decimal)   # type: pd.DataFrame
            df.Name = name
        elif file_extension == ".out":
            df = self.readOutFile(path)
            df.Name = name

        # listWidget.clear()

        for c in df.columns:
            if c.lower().strip().replace(" ", "-") not in ['time-step', 'flow-time']:
                if c not in self.columns:
                    self.columns.append(c)
                    
        self.dfs.append(df)

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
    
    def plotar(self):
        try:
            fig = go.Figure()

            df_count = 0
            for df in self.dfs:                    
                for coluna in self.listColunas.selectedItems():
                    if coluna.text() in df.columns:
                        fig.add_trace(
                            go.Scatter(x=df['flow-time'],
                                        y=df[coluna.text()],
                                        name=f"{df.Name}: {coluna.text()}",
                                        mode='lines+markers',
                                        marker_symbol=symbols[df_count],
                                        line=dict(dash=dash[df_count])
                                        )
                        ) 
                df_count += 1      
        

            fig.update_layout(title="Comparação de resultados",
                              xaxis_title='Tempos (s)',
                              yaxis_title='Amplitude',
                              legend=dict(
                                          orientation="h",
                                          yanchor="bottom",
                                          y=1.02,
                                         xanchor="right",
                                         x=1),
                              template='plotly_white'
                             )
        
            if (self.checkBoxHTML.isChecked() or 
                self.checkBoxCSV.isChecked() or 
                self.checkBoxPDF.isChecked() or
                self.checkBoxSVG.isChecked()):
                self.salvar(fig)

            fig.show()

            # mensagemSucesso()

        except Exception as e:
            mensagemErro(e)
            
    def salvar(self, fig: go.Figure):
        dialog = QFileDialog()
        directory = str(dialog.getExistingDirectory(self, "Selecione o diretório para salvar."))

        if directory != "":
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H%M%S")
            name = f"Comparacao_{now_str}"
            
            dialog = QInputDialog() # type: QInputDialog
            text, ok = dialog.getText(self, 'Nome do arquivo', 'Insira um nome para salvar o arquivo', text=name)
            if ok:
                name = text

            if self.checkBoxHTML.isChecked():
                fig.write_html(f"{directory}/{name}.html")

            if self.checkBoxPDF.isChecked():
                fig.write_image(f"{directory}/{name}.pdf")

            if self.checkBoxSVG.isChecked():
                fig.update_layout(
                    title = ""
                )
                fig.write_image(f"{directory}/{name}.svg")
            
            if self.checkBoxCSV.isChecked():
                columns = list()
                values = list()

                for d in fig.data:
                    columns.append(f"x:{d.name}")
                    columns.append(f"y:{d.name}")
                    values.append(d.x)
                    values.append(d.y)
                
                dfs = list()
                
                for c, v in zip(columns, values):
                    dfs.append(pd.DataFrame({c: v}))

                df = pd.concat(dfs, ignore_index=True, axis=1)
                df.columns = columns

                df.to_csv(f"{directory}/{name}.csv", sep=";", index=False, na_rep="NA")


        self.filename1 = None
        self.filename2 = None
        
def mensagemErro(e: Exception):
    print("{0}".format(e))
    msg = QMessageBox()
    msg.setMinimumWidth(200)
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Erro")
    msg.setInformativeText("{0}".format(e))
    msg.setWindowTitle("Erro")
    msg.exec_()


def mensagemSucesso():
    msg = QMessageBox()
    msg.setMinimumWidth(200)
    msg.setIcon(QMessageBox.Information)
    msg.setText("Plot gerado com sucesso.")
    # msg.setInformativeText("{0}".format(e))
    msg.setWindowTitle("Informação")
    msg.exec_()

