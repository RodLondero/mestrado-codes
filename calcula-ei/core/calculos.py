import pandas as pd
import numpy as np
import math, os

from matplotlib.ticker import (MultipleLocator)
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt

from .energia_incidente_astm import calc_by_ASTM


class Executar():

    def __init__(self, file_path: str, csv_sep: str = ";", csv_decimal: str = ","):
        self.file_path = file_path
        self.csv_sep = csv_sep
        self.csv_decimal = csv_decimal

        self.width = 10 
        self.height = 5

        self.run()

    def run(self):
        self.read_file()

        calc_by_ASTM(self.df)

        print(self.df)        

        self.fig = plt.figure(figsize=(self.width, self.height))    # type: figure.Figure
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

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier