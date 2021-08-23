import pandas as pd
import numpy as np


def calc_by_ASTM(df: pd.DataFrame, column: str = 1):
    A = 4.237312
    B = 6.715751
    C = -7.46962
    D = 3.339491
    E = 0.016389

    mmol = 63.546                       # g/mol
    massa = 18                          # g
    diametro = 4                        # cm
    area = np.pi * (diametro / 2) ** 2  # cm^2

    if type(column) == int:
        len_temp = len(df[df.columns[column]])
        tk = np.array(df[df.columns[column]])    # Temperatura em Kelvin
    elif type(column) == str:
        len_temp = len(df[column])
        tk = np.array(df[column])               # Temperatura em Kelvin
    else:
        raise Exception("Tipo do parâmetro 'columns' inválido.")

    tc = tk - 273.15                    # Temperatura em Celsius
    
    cp = np.zeros(len_temp)
    cp_medio = np.zeros(len_temp)
    Q = np.zeros(len_temp)
    
    for i in range(0, len_temp):
        tcp = tk[i] / 1000

        # Correção do calor específico
        cp[i] = (A + (B * tcp) + (C * (tcp ** 2)) +
                 (D * (tcp ** 3)) + (E / (tcp ** 2))) / mmol

        # Calor específico médio no intervalo considerado (cal/gºC)
        cp_medio[i] = (cp[0] + cp[i]) / 2

        # Energia Incidente no intervalo considerado (cal/cm²)
        # Q  = g * cal/gºC * ºC / cm^2
        Q[i] = (massa * cp_medio[i] * (tc[i] - tc[0]) / area)

    df['EI'] = Q

    return df
