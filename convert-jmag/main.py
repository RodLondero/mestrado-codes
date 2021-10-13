import sys
import pathlib
import os
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QLineEdit, QDialogButtonBox, QLabel, QInputDialog, QDoubleSpinBox, QToolButton, QMessageBox, QFileDialog
from PyQt5 import QtCore, uic


class App(QMainWindow):
    def __init__(self, path=None, parent=None):
        super(App, self).__init__()
        uic.loadUi(
            f'{pathlib.Path(__file__).parent.absolute()}/convert-jmag.ui', self)

        self.fileName = path
        self.df = None  # type: pd.DataFrame

        self.__findElements()
        self.__select_file()

        self.show()

    def __findElements(self):
        # ComboBox
        self.editArquivo = self.findChild(QLineEdit, 'editArquivo')  # type: QLineEdit
        self.btnArquivo = self.findChild(QToolButton, 'btnArquivo')  # type: QToolButton
        self.btnArquivo.clicked.connect(self.__select_file)
        self.cbUnidades = self.findChild(QComboBox, 'cbUnidades')  # type: QComboBox
        self.sbDiametro = self.findChild(QDoubleSpinBox, 'sbDiametro')  # type: QDoubleSpinBox
        self.btnDialog = self.findChild(QDialogButtonBox, 'btnDialog')  # type: QDialogButtonBox
        self.btnDialog.accepted.connect(self.event_ok)
        self.btnDialog.rejected.connect(self.event_cancel)

    def __select_file(self):
        
        try:
            self.__open_dialog_file()

            while True:
                if self.fileName:
                    filename, file_extension = os.path.splitext(self.fileName)
                    if file_extension == ".out":
                        self.df = self.__readFluentReportFiles()
                        break
                    elif file_extension == ".csv":
                        self.df = pd.read_csv(self.fileName, sep=';')
                        break
                    else:
                        msg = QMessageBox()
                        msg.setMinimumWidth(200)
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Erro")
                        msg.setInformativeText("Arquivo Inválido")
                        msg.setWindowTitle("Erro")
                        msg.exec_()
                        self.__open_dialog_file()
                else:
                    self.close()

            self.editArquivo.setText(self.fileName)
            # self.convert_jmag()

        except Exception as e:
            mensagem_erro(e)

    def event_ok(self):
        if self.editArquivo.text() == '':
            mensagem_erro("Selecione um arquivo.")
            return
        else:
            self.convert_jmag()

    def event_cancel(self):
        self.close()

    def convert_jmag(self):
        try:
            diametro = self.sbDiametro.value()
            unidade_conversao = (1e-3, 1e-2, 1)

            area = np.pi * (diametro*unidade_conversao[self.cbUnidades.currentIndex()] / 2) ** 2

            for c in self.df.columns:
                if c.lower() not in ['time step', 'time-step', 'flow-time']:
                    self.df[c] = self.df[c] * area

            self.df.to_csv(os.path.dirname(self.fileName) + "/current_sim.csv", sep=';', index=False)

            p = os.path.dirname(self.fileName).replace('/', '\\')
            msg = QMessageBox()
            msg.setMinimumWidth(200)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Sucesso")
            msg.setInformativeText("Arquivo convertido com sucesso.")
            msg.setWindowTitle("Sucesso")
            msg.exec_()
            os.system(f"D: && explorer.exe {p}")
        except Exception as e:
            mensagem_erro(e)
        
    def __readFluentReportFiles(self):
        # df_list = []
        file = self.fileName
        # for file in self.file_list:
        title = file.split(".")[0].split("\\")[-1]

        # if title in self.selectedFiles:
        print(f"Reading {file} ...")
        with open(file, 'r') as f:
            content = f.read().splitlines()

            # Get title
            # title = content[0].strip('"')

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
            # df_list.append(dataframe)

        return dataframe

    def __open_dialog_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Fluent Report Files (*.out);;CSV Files (*.csv)", options=options)
        self.fileName = fileName

    @staticmethod
    def titulo(texto):
        print("="*len(texto))
        print(texto)
        print("="*len(texto))


def mensagem_erro(e: Exception):
    print("{0}".format(e))
    msg = QMessageBox()
    msg.setMinimumWidth(200)
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Erro")
    msg.setInformativeText("{0}".format(e))
    msg.setWindowTitle("Erro")
    msg.exec_()


if __name__ == '__main__':
    diretorio = os.path.dirname(__file__)
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
