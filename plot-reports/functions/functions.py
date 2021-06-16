import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


def plot(file_name: str):
    fig = plt.figure(figsize=(9, 5))  # type: figure.Figure
    ax = plt.subplot()  # type: axes.Axes
    
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