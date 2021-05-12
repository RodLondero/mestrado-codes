from matplotlib.ticker import (MultipleLocator)
# from EnergiaIncidente import EnergiaIncidente
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import get_data_from_file, round_up


# Don't forget to change de results directory in "utils.py"

def main():
    fig = plt.figure(figsize=(10, 10))  # type: figure.Figure
    ax = fig.subplots(2, 3)

    plot_corrente('eletrodos_corrente.out', ax[0][0])
    plot_temperatura_fluido('fluido-temperatura.out', ax[0][1])
    plot_temperatura_calorimetro('termopar-temperatura.out', ax[0][2])
    plot_temperatura_calorimetro('calorimetro-temperatura-vol-med-rfile.out', ax[0][2], ls='dashed')
    # plot_energia_interna('calorimetro_energia_interna.out', ax[1][1])

    EI_ASTM = calc_by_ASTM(get_data_from_file('termopar-temperatura.out'))
    EI_Energia = calc_by_energia_interna(get_data_from_file('calorimetro_energia_interna.out'))

    # Plot EI pela ASTM
    plot_energia_incidente(EI_ASTM.copy(), ax[1][1], title="Energia Incidente (ASTM)")
    ax_ei = ax[1, 1]  # type: axes.Axes
    ax_ei.plot(float(EI_ASTM['flow-time'][-1:]) * 1000, float(EI_ASTM['EI'].max()), 'ko')
    ax_ei.annotate(f"{EI_ASTM['EI'].max():.4f} [$cal/cm^2$]",
                   xy=(float(EI_ASTM['flow-time'][-1:]) * 1000, float(EI_ASTM['EI'].max())),
                   xytext=(50, 8),
                   arrowprops=dict(arrowstyle="->"),
                   xycoords="data"
                   )
    ax_ei.legend(loc='upper left')
    # plot_energia_incidente(EI_ASTM.copy(),    ax[1][1], label="EI pela ASTM")
    # plot_energia_incidente(EI_Energia.copy(), ax[1][1], label="EI pela Energia Interna", title='Energia Incidente')

    ax[1, 0].axis('off')
    ax[1, 2].axis('off')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

    print(f"\nEnergia Incidente (ASTM): {EI_ASTM['EI'].max():.4f} [cal/cm^2]")


def plot_energia_incidente(df: pd.DataFrame, ax: axes.Axes, label: str = "Energia Incidente", title=""):
    df['flow-time'] = df['flow-time'] * 1000

    x = df['flow-time']
    y = df['EI']

    ax = df.plot(x='flow-time', y='EI', ax=ax,
                 title=title,
                 label=label,
                 xlabel='Tempo ($ms$)',
                 ylabel='Energia Incidente ($cal/cm^2$)',
                 #  xlim=(0, max(x)),
                 xlim=(0, 95),
                 ylim=(0, round_up(max(y))))

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(round_up(max(y), 0) / 10))
    ax.yaxis.set_minor_locator(MultipleLocator(round_up(max(y), 0) / 10 / 2))
    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)


def plot_corrente(file_name: str, ax: axes.Axes):
    corrente = get_data_from_file(file_name)

    corrente.rename(columns={'eletrodo_a_corrente': 'Corrente A'}, inplace=True)
    corrente.rename(columns={'eletrodo_b_corrente': 'Corrente B'}, inplace=True)
    corrente.rename(columns={'eletrodo_c_corrente': 'Corrente C'}, inplace=True)
    corrente['flow-time'] = corrente['flow-time'] * 1000

    ax = corrente.plot(x='flow-time', y=['Corrente A', 'Corrente B', 'Corrente C'], ax=ax,
                       title='Densidade de Corrente',
                       xlabel='Tempo ($ms$)',
                       ylabel='Corrente ($A/m^2$)',
                       xlim=(0, max(corrente['flow-time'])),
                       ylim=(0))
    ax.grid(b=True, ls='--', alpha=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))


def plot_temperatura_fluido(file_name: str, ax: axes.Axes):
    temperatura_fluido = get_data_from_file(file_name)
    temperatura_fluido.rename(columns={'fluido-temperatura': 'Temperatura'}, inplace=True)
    temperatura_fluido['flow-time'] = temperatura_fluido['flow-time'] * 1000

    ax = temperatura_fluido.plot(x='flow-time', y='Temperatura', ax=ax,
                                 title='Temperatura Máxima do Ar',
                                 xlabel='Tempo ($ms$)',
                                 ylabel='Temperatura ($K$)',
                                 xlim=(
                                     0, max(temperatura_fluido['flow-time'])),
                                 ylim=(0, max(temperatura_fluido['Temperatura'])))
    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(10000))
    ax.yaxis.set_minor_locator(MultipleLocator(5000))


def plot_temperatura_calorimetro(file_name: str, ax: axes.Axes, ls='solid'):
    temperatura_calorimetro = get_data_from_file(file_name).copy()

    for column in temperatura_calorimetro.columns:
        if column == 'calorimetro-temperatura-vol-med':
            temperatura_calorimetro.rename(columns={column: 'Tmed Volume'}, inplace=True)
        if column == 'termopar-temperatura':
            temperatura_calorimetro.rename(columns={column: 'T termopar'}, inplace=True)

    temperatura_calorimetro['flow-time'] = temperatura_calorimetro['flow-time'] * 1000

    ax = temperatura_calorimetro.plot(x='flow-time', y=temperatura_calorimetro.columns[1], ax=ax,
                                      title='Temperatura no Termopar',
                                      xlabel='Tempo ($ms$)',
                                      ylabel='Temperatura ($K$)',
                                      ls=ls,
                                      xlim=(0, max(temperatura_calorimetro['flow-time'])),
                                      #   ylim=(250)
                                      )
    #   ylim=(0))

    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.yaxis.set_minor_locator(MultipleLocator(25))


def plot_energia_interna(file_name: str, ax: axes.Axes):
    temperatura_fluido = get_data_from_file(file_name)
    temperatura_fluido.rename(columns={'calorimetro_energia_interna': 'Energia Interna'}, inplace=True)
    temperatura_fluido['flow-time'] = temperatura_fluido['flow-time'] * 1000

    x, y = 'flow-time', 'Energia Interna'

    ax = temperatura_fluido.plot(x=x, y=y, ax=ax,
                                 title='Energia Interna do Calorímetro',
                                 xlabel='Tempo ($ms$)',
                                 ylabel='Energia Interna ($K$)',
                                 xlim=(0, max(temperatura_fluido[x])),
                                 ylim=(0))
    ax.grid(b=True, which='major', ls='dashed', alpha=0.5)
    ax.grid(b=True, which='minor', ls='dotted', alpha=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))


def calc_by_ASTM(df: pd.DataFrame):
    A = 4.237312
    B = 6.715751
    C = -7.46962
    D = 3.339491
    E = 0.016389

    mmol = 63.546  # g/mol
    massa = 18  # g
    diametro = 4  # cm
    area = np.pi * (diametro / 2) ** 2  # cm^2
    len_temp = len(df[df.columns[1]])

    cp = np.zeros(len_temp)
    cp_medio = np.zeros(len_temp)
    Q = np.zeros(len_temp)

    tk = np.array(df[df.columns[1]])  # Temperatura em Kelvin
    tc = tk - 273.15  # Temperatura em Celsius

    for i in range(0, len_temp):
        tcp = tk[i] / 1000

        # Correção do calor específico
        cp[i] = (A + (B * tcp) + (C * (tcp ** 2)) + (D * (tcp ** 3)) + (E / (tcp ** 2))) / mmol

        # Calor específico médio no intervalo considerado (cal/gºC)
        cp_medio[i] = (cp[0] + cp[i]) / 2

        # Energia Incidente no intervalo considerado (cal/cm²)
        # Q  = g * cal/gºC * ºC / cm^2
        Q[i] = (massa * cp_medio[i] * (tc[i] - tc[0]) / area * 0.239)

    df['EI'] = Q

    return df


def calc_by_energia_interna(df: pd.DataFrame):
    # Cobre
    densidade = 8978
    cp = 381

    # Parâmetros do calorímetro
    area_face = 1255.5 / (10 ** 2)  # mm^2 -> cm^2
    volume = 2010.6 / (1000 ** 3)  # mm^3 -> m^3
    massa = densidade * volume  # kg = kg/m^3 * m^3

    massa_x_energia = [i * massa for i in df["calorimetro_energia_interna"]]

    df['EI'] = [i / area_face * 0.239 for i in massa_x_energia]

    return df


if __name__ == '__main__':
    main()
