import math

from matplotlib.ticker import (MultipleLocator)
# from EnergiaIncidente import EnergiaIncidente
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
results_directory = base_dir + "\\resultados\\"


def main():
    fig = plt.figure(figsize=(10, 10))  # type: figure.Figure
    ax = fig.subplots(2, 3)

    plot('eletrodos_corrente.out', ax[0][0])
    plot('fluido-temperatura.out', ax[0][1])
    plot('termopar-temperatura.out', ax[0][2], ylim=300)
    plot('calorimetro-temperatura-vol-med-rfile.out', ax[0][2], ylim=300)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot(file_name: str, ax: axes.Axes, ylim: int = 0):
    df = read_file(file_name)
    df['flow-time'] = df['flow-time'] * 1000

    ax = df.plot(x='flow-time', ax=ax,
                 title=df.name,
                 xlabel='Tempo ($ms$)',
                 xlim=(0, round_up(max(df['flow-time']), -1)),
                 ylim=ylim,
                 label=df.name)

    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    # ax.yaxis.set_major_locator(MultipleLocator(10000))
    # ax.yaxis.set_minor_locator(MultipleLocator(5000))


def read_file(filename: str):
    with open(results_directory + filename, 'r') as f:
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


if __name__ == '__main__':
    main()
