import os
import re
import sys
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
import plotly.graph_objs as go


class App(QMainWindow):

    def __init__(self, path: str = None):
        super().__init__()

        self.fileName = path
        self.df = None  # type: pd.DataFrame

        if not self.fileName:
            self.__select_file()

        if self.fileName:
            self.get_time_from_file()
        else:
            print("Selecione um arquivo.")

    def __select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Transcript Files (*.trn);;All Files (*)", options=options)
        self.fileName = fileName

    def get_time_from_file(self):
        filename, extension = os.path.splitext(self.fileName)

        # Definição dos padrões
        pattern_seconds = "t_sec:\s([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\ss"
        pattern_minutes = "t_min:\s([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\smin"
        pattern_hour = "t_h:\s+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\sh"
        pattern_time_step = "Time-Step:\s+[0-9]+"

        # Inicialização das listas
        time_step = list()
        t_sec = list()
        t_min = list()
        t_h = list()

        # Realiza a busca dos tempos
        for i, line in enumerate(open(self.fileName)):
            check_pattern(pattern_time_step, line, time_step)
            check_pattern(pattern_seconds, line, t_sec)
            check_pattern(pattern_minutes, line, t_min)
            check_pattern(pattern_hour, line, t_h)

        # Salva em um DataFrame
        self.df = pd.DataFrame(list(zip(time_step, t_sec, t_min, t_h)), columns=[
                               'time-step', 't_sec', 't_min', 't_h'])
        # self.df.set_index('time-step', inplace=True)

        # Imprime na tela os TOTAIS e a MÉDIA
        print("Total")
        print(self.df.sum())

        print("\nMédia")
        print(self.df.mean())

        # Plot dos tempos
        opcao = input(
            "\nDeseja visualizar o gráfico de minutos por passo (S/[N])?").lower()
        if opcao == 's':
            self.plot()

    def plot(self):
        msg = "Escolha a opção para plotar: "
        self.titulo(msg)

        while True:
            for i, c in enumerate(self.df.columns[1:]):
                print(f"{i+1} - {c}")
            print('0 - Sair')

            print("="*len(msg))
            opcao = str(input("Opção: "))
            opcao = -1 if not opcao.isdecimal() else int(opcao)

            if opcao in (1, 2, 3):
                coluna = self.df.columns[opcao]

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(x=self.df['time-step'],
                               y=self.df[coluna],
                               name=coluna,
                               mode='lines'
                               )
                )
                fig.update_layout(
                    # X Axis configuration
                    xaxis=dict(
                        title='Time-Step',
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
                        title=coluna,
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
                        type='linear'
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1),
                    template='simple_white'
                )
                fig.show()
                # self.df.plot(y = coluna)
                # plt.ylabel(coluna)
                # plt.xlabel("Time Step")
                # plt.grid(True, which="both")
                # plt.show()

                exit()
            elif opcao == 0:
                exit()
            else:
                print("Opção inválida")

    @staticmethod
    def titulo(texto):
        print("="*len(texto))
        print(texto)
        print("="*len(texto))


def check_pattern(pattern: str, line: str, lista: list):
    for match in re.finditer(pattern, line):
        lista.append(float(match.group().strip().split()[1]))


if __name__ == '__main__':
    diretorio = os.path.dirname(__file__)
    # path = os.path.join(diretorio, "_HOA_4.16kV_Malha_01_300_pontos_init.trn")

    app = QApplication(sys.argv)
    ex = App()
