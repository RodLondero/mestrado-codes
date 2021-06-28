from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

import pandas as pd
import sys, os, csv
import plotly.express as px
import plotly.graph_objs as go
import pathlib

pathdir = pathlib.Path(__file__).parent.absolute()

class Ui(QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/window.ui', self)  # Load the .ui file
        
        # Edits
        self.lineEdit          = self.findChild(QLineEdit, 'lineEdit')          # type: QLineEdit
        self.lineEdit2         = self.findChild(QLineEdit, 'lineEdit2')         # type: QLineEdit

        # Lists
        self.list1 = self.findChild(QListWidget, 'listWidget')     # type: QListWidget
        self.list1.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.list2 = self.findChild(QListWidget, 'listWidget2')    # type: QListWidget
        self.list2.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Buttons
        self.btnFileDialog1 = self.findChild(QPushButton, 'btnFileDialog1')
        self.btnFileDialog1.clicked.connect(lambda: self.openFileDialog(self.lineEdit, self.list1))

        self.btnFileDialog2 = self.findChild(QPushButton, 'btnFileDialog2')
        self.btnFileDialog2.clicked.connect(lambda: self.openFileDialog(self.lineEdit2, self.list2))

        self.btnAbrir1 = self.findChild(QPushButton, 'btnAbrir1')
        self.btnAbrir1.clicked.connect(lambda: self.abrirArquivos(self.lineEdit, self.list1))

        self.btnAbrir2 = self.findChild(QPushButton, 'btnAbrir2')
        self.btnAbrir2.clicked.connect(lambda: self.abrirArquivos(self.lineEdit2, self.list2))

        self.btnPlot = self.findChild(QPushButton, 'btnPlot')
        self.btnPlot.clicked.connect(self.plotar)

        # ComboBox
        self.comboBoxSep1     = self.findChild(QComboBox, 'comboBoxSep1')       # type: QComboBox
        self.comboBoxSep2     = self.findChild(QComboBox, 'comboBoxSep2')       # type: QComboBox
        self.comboBoxDecimal1 = self.findChild(QComboBox, 'comboBoxDecimal1')   # type: QComboBox
        self.comboBoxDecimal2 = self.findChild(QComboBox, 'comboBoxDecimal2')   # type: QComboBox

        # CheckBox
        self.checkBoxHTML = self.findChild(QCheckBox, 'checkBoxHTML') # type: QCheckBox
        self.checkBoxCSV  = self.findChild(QCheckBox, 'checkBoxCSV')  # type: QCheckBox       
        self.checkBoxPDF  = self.findChild(QCheckBox, 'checkBoxPDF')  # type: QCheckBox
        self.checkBoxSVG  = self.findChild(QCheckBox, 'checkBoxSVG')  # type: QCheckBox
        
        # Configs
        self.setMinimumSize(635, 385)
        self.setFixedSize(635, 385)
        self.setWindowTitle('Comparação de resultados')
        
        self.filename1 = None
        self.filename2 = None

        self.show()  # Show the GUI

    def openFileDialog(self, lineEdit: QLineEdit, listWidget: QListWidget):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Abrir arquivo", lineEdit.text(), "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            lineEdit.setText(fileName)

    def abrirArquivos(self, lineEdit: QLineEdit, listWidget: QListWidget):
        try:
            fileName = lineEdit.text()

            if fileName == "":
                raise Exception("Selecione um arquivo para abrir")
            self.getFileColumns(path=fileName, listWidget=listWidget)
        except Exception as e:
            mensagemErro(e)

    def getFileColumns(self, path: str, listWidget: QListWidget):

        if listWidget.objectName() == self.list1.objectName():
            separador = " " if str(self.comboBoxSep1.currentText()) == "Espaço" else str(self.comboBoxSep1.currentText()) 
            decimal = str(self.comboBoxDecimal1.currentText())

        if listWidget.objectName() == self.list2.objectName():
            separador = " " if str(self.comboBoxSep2.currentText()) == "Espaço" else str(self.comboBoxSep1.currentText()) 
            decimal = str(self.comboBoxDecimal2.currentText())

        _, file_extension = os.path.splitext(path)

        if file_extension == ".csv":
            df = pd.read_csv(path, sep=separador, decimal=decimal)   # type: pd.DataFrame
        elif file_extension == ".out":
            df = self.readOutFile(path)

        listWidget.clear()

        for c in df.columns:
            if c.lower().strip().replace(" ", "-") not in ['time-step', 'flow-time']:
                listWidget.addItem(c)

        if listWidget.objectName() == self.list1.objectName():
            self.df1 = df   # type: pd.DataFrame
        if listWidget.objectName() == self.list2.objectName():
            self.df2 = df   # type: pd.DataFrame


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
            if self.lineEdit.text() == "" and self.lineEdit2.text() == "":
                raise Exception("Selecione 2 arquivos para comparar")

            fig = go.Figure()

            if not self.list1.selectedItems() and not self.list2.selectedItems():
                raise Exception("Selecione algo para plotar")

            titulo = "Comparação: "
            if self.list1.selectedItems():
                self.filename1 = os.path.basename(self.lineEdit.text()).split(".")[0]
                
                if titulo != "Comparação: ":
                    titulo += " x "                
                titulo += self.filename1

                for item in self.list1.selectedItems():
                    fig.add_trace(
                        go.Scatter(x=self.df1['flow-time'],
                                   y=self.df1[item.text()],
                                   name=f"{self.filename1}: {item.text()}",
                                   mode='lines+markers',
                                   marker_symbol='circle'
                                   #    line=dict(color='black', width=2)
                                   )
                    )

            if self.list2.selectedItems():
                self.filename2 = os.path.basename(self.lineEdit2.text()).split(".")[0]

                if titulo != "Comparação: ":
                    titulo += " x "                
                titulo += self.filename2

                for item in self.list2.selectedItems():
                    fig.add_trace(
                        go.Scatter(x=self.df2['flow-time'],
                                   y=self.df2[item.text()],
                                   name=f"{self.filename2}: {item.text()}",
                                   mode='lines+markers',
                                   marker_symbol='diamond',
                                   line=dict(dash='dot')
                                   )
                    )

            fig.update_layout(title=titulo,
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

            mensagemSucesso()

        except Exception as e:
            mensagemErro(e)
    

    def salvar(self, fig: go.Figure):
        dialog = QFileDialog()
        directory = str(dialog.getExistingDirectory(self, "Selecione o diretório para salvar."))

        if directory != "":
            name = f"Comparacao_"

            if self.filename1:
                name += self.filename1
            if self.filename2:
                name += "_" + self.filename2
            
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

