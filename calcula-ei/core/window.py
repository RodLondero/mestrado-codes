import math
import os
import pathlib
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QToolButton, QComboBox, QCheckBox, QListWidget, QRadioButton, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow, QPushButton
from plotly.subplots import make_subplots

from .calc_ei import calc_by_ASTM, calc_by_energia_interna

pathdir = pathlib.Path(__file__).parent.absolute()


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/window.ui', self)

        self.initUI()

    def initUI(self):
        """ Initializes the window """

        self.setWindowTitle("Calculo de Energia Incidente")
        self.setMinimumSize(600, 300)
        self.setFixedSize(600, 300)

        self.getComponents()
        self.setCommands()

        self.show()
        self.openFileNameDialog()

    def getComponents(self):
        """ Find components in window.ui and set to self variables """
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
        """ Set actions to window elements """
        self.btnFile.clicked.connect(self.openFileNameDialog)
        self.btnCalcular.clicked.connect(self.calcular_ei)
        self.btnAbrir.clicked.connect(self.abrirArquivos)
        self.comboBoxSep.currentTextChanged.connect(self.abrirArquivos)
        self.comboBoxDecimal.currentTextChanged.connect(self.abrirArquivos)
        self.lineEdit.textChanged.connect(self.abrirArquivos)

    def openFileNameDialog(self):
        """ Open FileDialog and get the full path of a file """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 
                                                 "Select a report file", 
                                                 "",
                                                 "Report Files (*.csv *.out);; All Files (*)", 
                                                 options=options)
        if fileName:
            self.lineEdit.setText(fileName)

    def abrirArquivos(self):
        """ Open the selected file and get it columns """
        try:
            fileName = self.lineEdit.text()

            # Check if the file is selected
            if fileName == "":
                raise Exception("Selecione um arquivo para abrir")

            # Set the separator and decimal mark
            separador = " " if str(self.comboBoxSep.currentText()) == "Espaço" else str(self.comboBoxSep.currentText())
            decimal = str(self.comboBoxDecimal.currentText())

            # Get the file extension
            _, file_extension = os.path.splitext(fileName)

            # Open the file
            if file_extension == ".csv":
                self.df = pd.read_csv(fileName, sep=separador, decimal=decimal)  # type: pd.DataFrame
            elif file_extension == ".out":
                self.df = self.readOutFile(fileName)

            # Clear the list with the columns
            self.list1.clear()

            # Get the columns from file
            for c in self.df.columns:
                if c.lower().strip().replace(" ", "-") not in ['time-step', 'flow-time']:
                    self.list1.addItem(c)

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro")
            msg.setInformativeText("{0}".format(e))
            msg.setWindowTitle("Erro")
            msg.exec_()

    def readOutFile(self, filename: str):
        """ Read a .out file """
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

    def calcular_ei(self):
        """ Calculate the Incident Energy """
        try:
            # Check if the file is selected
            if self.lineEdit.text() == "":
                raise Exception("Selecione um arquivo.")

            # Check if an item is selected
            if not self.list1.selectedItems():
                raise Exception("Selecione uma coluna")

            path = self.lineEdit.text()
            separador = " " if str(self.comboBoxSep.currentText()) == "Espaço" else str(self.comboBoxSep.currentText())
            decimal = str(self.comboBoxDecimal.currentText())

            selecao = self.list1.selectedItems()[0].text()
            # Calc EI using ASTM 
            if self.radioButtonASTM.isChecked():
                self.df['EI'] = calc_by_ASTM(self.df[selecao].tolist())
            elif self.radioButtonEnergia.isChecked():
                self.df['EI'] = calc_by_energia_interna(self.df[selecao].tolist())

            # Show the results
            # self.showResults()

            # Get the max EI
            max_EI = f"{self.df['EI'].max():.4f} [cal/cm^2]"

            # Print the max EI
            print(f"\nMáxima EI: {max_EI}")

            # Make a plot
            self.plot()

            # Show a message with the max EI
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

    def plot(self, **kwargs):
        """ Make the plot using Plotly """

        df = self.df.copy()

        fig = make_subplots(rows=1, cols=2)

        # Add the first plot related to Temperature
        fig.add_trace(
            go.Scatter(x=df['flow-time'], y=df[self.list1.selectedItems()[0].text()], name="Temperatura"),
            row=1, col=1)

        # Add the second plot related to EI
        fig.add_trace(
            go.Scatter(x=df['flow-time'], y=df['EI'], name="Energia Incidente"),
            row=1, col=2)

        # Add an annotation to show the maximum EI
        fig.add_annotation(x=df['flow-time'].iat[-1], y=df['EI'].iat[-1],
                           text=f"{df['EI'].iat[-1]:.4f}",
                           showarrow=True,
                           arrowhead=1,
                           row=1, col=2)

        # Some configuration for the plot
        fig.update_layout(title_text="Energia Incidente")

        # Save the data if some checkbox is checked
        if (self.checkBoxHTML.isChecked() or 
            self.checkBoxCSV.isChecked() or 
            self.checkBoxPDF.isChecked() or
            self.checkBoxSVG.isChecked()):
            self.salvar(fig)

        # Show the plot
        fig.show()

    def salvar(self, fig: go.Figure):
        """ Save the Temperature and EI """

        # Select the directory to save the file
        dialog = QFileDialog()
        directory = str(dialog.getExistingDirectory(self, "Selecione o diretório para salvar."))

        # IF the directory is selected
        if directory != "":
            # Generate a default name for the file with datetime
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H%M%S")
            name = f"Energia_Incidente_{now_str}"

            # Set the name to file
            dialog = QInputDialog()  # type: QInputDialog
            text, ok = dialog.getText(self, 'Nome do arquivo', 'Insira um nome para salvar o arquivo', text=name)
            if ok:
                name = text

            # Save the plot in HTML file
            if self.checkBoxHTML.isChecked():
                fig.write_html(f"{directory}/{name}.html")

            # Save the plot in PDF file
            if self.checkBoxPDF.isChecked():
                fig.write_image(f"{directory}/{name}.pdf")

            # Save the plot in SVG file
            if self.checkBoxSVG.isChecked():
                fig.update_layout(title="")
                fig.write_image(f"{directory}/{name}.svg")

            # Save the data in CSV file
            if self.checkBoxCSV.isChecked():
                coluna = self.list1.currentItem().text()
                self.df.to_csv(f"{directory}/{name}.csv",
                               sep=";",
                               columns=['flow-time', coluna, 'EI'],
                               index=False,
                               na_rep="NA")

        self.filename1 = None
        self.filename2 = None

    def get_max_EI(self):
        """ Return the maximum EI """
        return self.df['EI'].max()


def round_up(n, decimals=0):
    """ Round up to the next 10^n

    Args:
        n (number): the number it will be rounded
        decimals (int, optional): decimal number to round. Defaults to 0.

    Returns:
        (float): number rounded up to the next 10^n
    """
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
