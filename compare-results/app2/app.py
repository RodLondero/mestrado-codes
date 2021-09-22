import os
import pathlib
import random
import re
import time
from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QListWidget, QSlider, QToolButton, QPushButton, QComboBox, QCheckBox, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QInputDialog, QMessageBox

pathdir = pathlib.Path(__file__).parent.absolute()

symbols = ['circle', 'square', 'triangle-up', 'cross', 'star']
dash = ["dot", "dash", "dashdot", "longdash", "longdashdot"]


class Ui(QMainWindow):
    def __init__(self, root_path: str = None):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/window.ui', self)  # Load the .ui file

        self.setFixedSize(1030, 400)

        self.__findElements()

        self.dfs = list()
        self.columns = list()
        self.filename2 = None
        self.filename1 = None
        self.total = dict()

        self.editPasta.setText(root_path)
        self.load_files(root_path)

        self.show()

    def __findElements(self):
        # Edits
        self.editPasta  = self.findChild(QLineEdit, 'editPasta')          # type: QLineEdit
        self.editFiltro = self.findChild(QLineEdit, 'editFiltro')         # type: QLineEdit
        self.editFiltro.textChanged.connect(self.on_textChanged)
        self.editFiltroColunas = self.findChild(QLineEdit, 'editFiltroColunas')  # type: QLineEdit
        self.editFiltroColunas.textChanged.connect(self.on_textChangedColunas)

        # Lists
        self.listArquivos = self.findChild(QListWidget, 'listArquivos')  # type: QListWidget
        self.listArquivos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listArquivos.itemSelectionChanged.connect(self.reset_column_list)

        self.listColunas = self.findChild(QListWidget, 'listColunas')  # type: QListWidget
        self.listColunas.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Buttons
        self.btnPasta = self.findChild(QToolButton, 'btnPasta')  # type: QToolButton
        self.btnPasta.clicked.connect(self._open_folder_dialog)

        self.btnAbrir = self.findChild(QPushButton, 'btnAbrir')  # type: QPushButton
        self.btnAbrir.clicked.connect(self.click_abrir)
        self.btnPlotar = self.findChild(QPushButton, 'btnPlotar')  # type: QPushButton
        self.btnPlotar.clicked.connect(self.click_plotar)
        self.btnAtualizar = self.findChild(QPushButton, 'btnAtualizar')  # type: QPushButton
        self.btnAtualizar.clicked.connect(self.click_atualizar)

        # ComboBox
        self.comboSep = self.findChild(QComboBox, 'comboSep')  # type: QComboBox
        self.comboSep.currentTextChanged.connect(self.click_abrir)
        self.comboDecimal = self.findChild(QComboBox, 'comboDecimal')  # type: QComboBox
        self.comboDecimal.currentTextChanged.connect(self.click_abrir)
        self.comboOpcoes = self.findChild(QComboBox, 'comboOpcoes')  # type: QComboBox

        # CheckBox
        self.checkBoxHTML = self.findChild(QCheckBox, 'checkBoxHTML')  # type: QCheckBox
        self.checkBoxCSV  = self.findChild(QCheckBox, 'checkBoxCSV')   # type: QCheckBox
        self.checkBoxPDF  = self.findChild(QCheckBox, 'checkBoxPDF')   # type: QCheckBox
        self.checkBoxSVG  = self.findChild(QCheckBox, 'checkBoxSVG')   # type: QCheckBox
        
        # Slider
        self.labelMin = self.findChild(QLabel, 'labelMin')  # type: QLabel
        self.labelMax = self.findChild(QLabel, 'labelMax')  # type: QLabel
        
        self.sliderMin = self.findChild(QSlider, 'sliderMin')  # type: QSlider
        self.sliderMin.valueChanged.connect(self.on_sliderMin_valueChanged)

        self.sliderMax = self.findChild(QSlider, 'sliderMax')  # type: QSlider
        self.sliderMax.valueChanged.connect(self.on_sliderMax_valueChanged)

    def _open_folder_dialog(self):
        fname = QFileDialog.getExistingDirectory(self, "Selecione o diretório.")
        if fname != "":
            self.editPasta.setText(fname + "/")
            self.load_files(fname)

    def on_sliderMin_valueChanged(self):
        val = self.sender().value()
        # val = round(val * self.slider_max_val / self.slider_max_it, 7)
        self.labelMin.setText(f"Min: ({val})")

    def on_sliderMax_valueChanged(self):
        val = self.sender().value()
        # val = round(val * self.slider_max_val / self.slider_max_it, 7)
        self.labelMax.setText(f"Max: ({val})")

    @QtCore.pyqtSlot(str)
    def on_textChanged(self, text: str):
        for row in range(self.listArquivos.count()):
            it = self.listArquivos.item(row)
            # widget = self.listArquivos.itemWidget(it)
            if text:
                it.setHidden(not self.filter(text.lower(), it.text().lower()))
            else:
                it.setHidden(False)

    @QtCore.pyqtSlot(str)
    def on_textChangedColunas(self, text: str):
        for row in range(self.listColunas.count()):
            it = self.listColunas.item(row)
            # widget = self.listArquivos.itemWidget(it)
            if text:
                it.setHidden(not self.filter(text.lower(), it.text().lower()))
            else:
                it.setHidden(False)

    @staticmethod
    def filter(text, keywords):
        text = text.split(" ")
        regex = ""
        for f in text:
            regex += f"(?=.*{f})"
        
        x = re.search(f"{regex}", keywords, re.IGNORECASE)
        if x:
            return x.string
        # return text in keywords

    def load_files(self, fname):
        self.listArquivos.clear()
        for f in os.listdir(fname):
            if f.endswith(".out") or f.endswith('.csv') or f.endswith('.trn'):
                self.listArquivos.addItem(f)

        for f in os.scandir(fname):
            if f.is_dir():
                for arquivo in os.listdir(f.path):
                    if arquivo.endswith(".out") or arquivo.endswith('.csv') or arquivo.endswith('.trn'):
                        self.listArquivos.addItem(f.name + "\\" + arquivo)

        self.listArquivos.sortItems()

    def click_atualizar(self):
        try:
            if self.editPasta.text() == "":
                raise Exception("Selecione uma pasta.")

            selectedItems = list()
            for item in self.listArquivos.selectedItems():
                selectedItems.append(item.text())

            self.load_files(self.editPasta.text())

            # self.listArquivos.setSelectionMode(QListWidget.MultiSelection)
            for i in selectedItems:
                matching_items = self.listArquivos.findItems(i, QtCore.Qt.MatchExactly)
                # self.listArquivos.setCurrentItem(i)
                for item in matching_items:
                    item.setSelected(True)

        except Exception as e:
            mensagem_erro(e)

    def click_plotar(self):
        try:
            if not self.listColunas.selectedItems():
                raise Exception("Selecione uma coluna para plotar")

            self.plotar()
        except Exception as e:
            mensagem_erro(e)

    def reset_column_list(self):
        self.listColunas.clear()

    def click_abrir(self):
        try:
            if self.editPasta.text() == "":
                raise Exception("Selecione um arquivo para abrir")

            self.dfs.clear()
            self.listColunas.clear()
            self.columns.clear()

            selectedItems = list()
            for item in self.listArquivos.selectedItems():
                selectedItems.append(item.text())
            selectedItems.sort(reverse=False)

            for arquivo in selectedItems:
                path = os.path.join(self.editPasta.text(), arquivo)
                self.get_file_columns(path, arquivo)

            self.listColunas.addItems(self.columns)

            max_it = 0
            for df in self.dfs:
                number_of_rows = len(df.index)
                if number_of_rows > max_it:
                    max_it = number_of_rows

            self.sliderMin.setMaximum(max_it)
            self.sliderMax.setMaximum(max_it)
            self.sliderMax.setValue(max_it)

        except Exception as e:
            mensagem_erro(e)

    def get_file_columns(self, path: str, name: str = None):

        _, file_extension = os.path.splitext(path)

        if name.find("\\") != -1 or name.find("/") != -1:
            name, _ = os.path.splitext(name)
            name = name.replace("/", "\\")
            name = name.split("\\")[0]

        if file_extension == ".csv":
            separador = " " if str(self.comboSep.currentText()) == "Espaço" else str(self.comboSep.currentText())
            decimal = str(self.comboDecimal.currentText())

            df = pd.read_csv(path, sep=separador, decimal=decimal)  # type: pd.DataFrame
            df.Name = name
        elif file_extension == ".out":
            df = self.reat_out_files(path)
            df.Name = name

        elif file_extension == ".trn":
            pattern_data = re.compile(
                "^(\s+(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\s+)+)(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)\s+[0-9]+$")
            pattern_title = re.compile(
                "^(\s+([a-zA-Z]+\s+)+)[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]+\s+k\s+[a-zA-Z]+\s+[a-zA-Z]+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\s+p1\s+[a-zA-Z]+/[a-zA-Z]+$")

            columns = []
            lines = []

            start_time = time.time()

            for i, line in enumerate(open(path)):
                # Get title columns
                if not columns:
                    for match in re.finditer(pattern_title, line):
                        print("Getting titles...")
                        columns = self.get_titles(match.group())

                # Get data
                for match in re.finditer(pattern_data, line):
                    result = match.group().strip().split()

                    # Format values to Float
                    for i in range(0, len(result[:-2])):
                        result[i] = float(result[i])
    
                    if (int(result[0]) % 1000 == 0) and int(result[-1]) != 0:
                        print(f"Getting iteration: {result[0]}")

                    lines.append(result)

            # Create a DataFrame and convert data to float
            df = pd.DataFrame(data=lines, columns=columns)
            # df.set_index("iter")
            df.Name = name

            del (df['time'])

        # listWidget.clear()

        for c in df.columns:
            if c.lower().strip().replace(" ", "-") not in ['time-step', 'flow-time', 'iter']:
                if c not in self.columns:
                    self.columns.append(c)

        self.dfs.append(df)

    @staticmethod
    def get_titles(line: str):
        titles_list = line.replace("/", " ").strip().split(" ")
        titles_list[-1] = 'iteration'

        titles = []
        for title in titles_list:
            if title != "":
                titles.append(title)

        return titles.copy()

    @staticmethod
    def reat_out_files(filename: str):

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

    def get_mode(self):
        if self.comboOpcoes.currentIndex() == 0:
            return "lines+markers"
        elif self.comboOpcoes.currentIndex() == 1:
            return "lines"
        else:
            return "markers"

    def plotar(self):
        try:
            if self.sliderMin.value() > self.sliderMax.value():
                raise Exception("O valor mínimo não pode ser maior que o valor máximo.")

            fig = go.Figure()

            self.total = dict()

            df_count = 0
            for df in self.dfs:
                name = df.Name
                df = df.loc[self.sliderMin.value():self.sliderMax.value()].copy()
                for coluna in self.listColunas.selectedItems():
                    if coluna.text() in df.columns:
                        self.total[f"{name}_{coluna.text()}"] = df[coluna.text()].count()
                        fig.add_trace(
                            go.Scatter(x=df['flow-time'] if 'flow-time' in df.columns else df['iter'],
                                       y=df[coluna.text()],
                                       name=f"{name}: {coluna.text()}",
                                       mode=self.get_mode(),
                                       marker_symbol=random.choice(symbols),
                                       line=dict(dash="solid" if df_count == 0 else random.choice(dash))
                                       )
                        )
                df_count += 1

            fig.update_layout(title="Comparação de resultados",
                              # X Axis configuration  
                              xaxis=dict(
                                  title='Tempo (s)' if 'flow-time' in df.columns else 'Iterações',
                                  # Grid
                                  showgrid=True,
                                  # Zero line
                                  zeroline=False,
                                  # Exponent format
                                  showexponent='all',
                                  exponentformat='none',
                                  # Border
                                  showline=True,
                                  linewidth=1,
                                  linecolor='black',
                                  mirror=True,
                                  #
                                #   rangemode="tozero"
                              ),
                              # X Axis configuration
                              yaxis=dict(
                                  title='Amplitude',
                                  # Grid
                                  showgrid=True,
                                  # Zero line
                                  zeroline=False,
                                  # Exponent format
                                  showexponent='all',
                                  exponentformat='power',
                                  # Border
                                  showline=True,
                                  linewidth=1,
                                  linecolor='black',
                                  mirror=True,
                                  # Type: linear or log
                                  type='linear' if 'flow-time' in df.columns else 'log'
                              ),
                              legend=dict(
                                  orientation="v",
                                #   yanchor="bottom",
                                #   y=1.02,
                                #   xanchor="right",
                                #   x=1
                            ),
                              template='simple_white'
                              )

            if (self.checkBoxHTML.isChecked() or
                    self.checkBoxCSV.isChecked() or
                    self.checkBoxPDF.isChecked() or
                    self.checkBoxSVG.isChecked()):
                self.salvar(fig)

            for key, value in self.total.items():
                print(f"{key}: {value}")
            fig.show()

        except Exception as e:
            mensagem_erro(e)

    def salvar(self, fig: go.Figure):
        dialog = QFileDialog()
        directory = str(dialog.getExistingDirectory(self, "Selecione o diretório para salvar."))

        if directory != "":
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H%M%S")
            name = f"Comparacao_{now_str}"

            dialog = QInputDialog()  # type: QInputDialog
            text, ok = dialog.getText(self, 'Nome do arquivo', 'Insira um nome para salvar o arquivo', text=name)
            if ok:
                name = text

            if self.checkBoxHTML.isChecked():
                fig.write_html(f"{directory}/{name}.html")

            if self.checkBoxPDF.isChecked():
                fig.write_image(f"{directory}/{name}.pdf")

            if self.checkBoxSVG.isChecked():
                fig.update_layout(
                    title=""
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


def mensagem_erro(e: Exception):
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
