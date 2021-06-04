import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from src.calculos import *
from matplotlib import rcParams

# Local onde estão os dados
data_path = './data/parametros.xlsx'

# Configurações padrão dos plots
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams['font.size'] = 11
rcParams['figure.figsize'] = [18/2.54, 10/2.54]

def plotDensity(save_fig = False):
    dados = pd.read_excel(data_path, sheet_name="Density", engine="openpyxl")

    dados
    tmin, tmax = 300, 30000
    t = np.arange(tmin+50, tmax+50, 50)
    density = getDensity(t, dados)

    fig = plt.figure()
    fig.canvas.set_window_title('Density')

    plt.plot(t, density, linewidth=2)

    plt.xlabel("Temperature (K)")
    plt.xlim(left=0, right=tmax)
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True)))

    plt.ylabel("Mass Density (Kg/m³)")
    plt.ylim(bottom=0, top=max(density))

    plt.minorticks_on()
    plt.grid(b=True, which='major', linestyle='-', alpha=0.3)
    plt.grid(b=True, which='minor', linestyle='-', alpha=0.3)
    plt.tight_layout()

    if save_fig:
        fig.savefig("{}{}{}".format(save_fig['local'], 'density', save_fig['tipo']))
        
def plotSpecificHeat(save_fig = False):
    dados = pd.read_excel(data_path, sheet_name="Specific_Heat", engine="openpyxl")
            
    tmin, tmax = 300, 30000
    t = np.arange(tmin, tmax+50, 50)
    specific_heat = getSpecificHeat(t, dados)
    
    fig = plt.figure()
    fig.canvas.set_window_title('Specific Heat')

    plt.plot(t, specific_heat, linewidth=2)
    
    plt.xlabel("Temperature (K)")
    plt.xlim(left=0, right=tmax)
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True)))

    plt.ylabel("Specific Heat (J/Kg.K)")
    plt.ylim(bottom=0, top=max(specific_heat)+1000)
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True))) 
    
    plt.minorticks_on()
    plt.grid(b=True, which='major', linestyle='-', alpha=0.3)
    plt.grid(b=True, which='minor', linestyle='-', alpha=0.3)
    plt.tight_layout()
    
    if save_fig:
        fig.savefig("{}{}{}".format(save_fig['local'], 'specific_heat', save_fig['tipo']))

def plotViscosity(save_fig = False):
    dados = pd.read_excel(data_path, sheet_name="Viscosity", engine="openpyxl")
    
    tmin, tmax = 3000, 30000
    t = np.arange(tmin, tmax, 50)
    viscosity = getViscosity(t, dados)
    
    fig = plt.figure()
    fig.canvas.set_window_title('Viscosity')
    
    plt.plot(t, viscosity, linewidth=2)
    
    plt.xlabel("Temperature (K)")
    plt.xlim(left=0, right=tmax)
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True)))

    plt.ylabel("Viscosity")
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%2.2e", x, grouping=True))) 
    
    plt.minorticks_on()
    plt.grid(b=True, which='major', linestyle='-', alpha=0.3)
    plt.grid(b=True, which='minor', linestyle='-', alpha=0.3)
    plt.tight_layout()
    
    if save_fig:
        fig.savefig("{}{}{}".format(save_fig['local'], 'viscosity', save_fig['tipo']))
        
def plotThermalCondutivity(save_fig = False):
    dados = pd.read_excel(data_path, sheet_name="Thermal_Conductivity", engine="openpyxl") 
        
    tmin, tmax = 300, 30000
    t = np.arange(tmin, tmax+50, 50)
    thermal_condutivity = getThermalCondutivity(t, dados)
    
    fig = plt.figure()
    fig.canvas.set_window_title('Thermal Condutivity')
    
    plt.plot(t, thermal_condutivity, linewidth=2)
    
    plt.xlabel("Temperature (K)")
    plt.xlim(left=0, right=tmax)
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True)))

    plt.ylabel("Thermal Condutivity")
    #plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True))) 
    
    plt.minorticks_on()
    plt.grid(b=True, which='major', linestyle='-', alpha=0.3)
    plt.grid(b=True, which='minor', linestyle='-', alpha=0.3)
    plt.tight_layout()
    
    if save_fig:
        fig.savefig("{}{}{}".format(save_fig['local'], 'thermal_condutivity', save_fig['tipo']))
        
def plotElectricalCondutivity(save_fig = False):
    dados = pd.read_excel(data_path, sheet_name="Electrical_Conductivity", engine="openpyxl")
                    
    tmin, tmax = 300, 30000
    t = np.arange(tmin, tmax, 50)
    electrical_condutivity = getElectricalCondutivity(t, dados)
    
    fig = plt.figure()
    fig.canvas.set_window_title('Electrical Condutivity')
    
    plt.plot(t, electrical_condutivity, linewidth=2)
    
    plt.xlabel("Temperature (K)")
    plt.xlim(left=0, right=tmax)
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: locale.format_string("%d", x, grouping=True)))

    plt.ylabel("Electrical Condutivity")
    plt.ylim(bottom=0, top=max(electrical_condutivity)+1000)

    plt.minorticks_on()
    plt.grid(b=True, which='major', linestyle='-', alpha=0.3)
    plt.grid(b=True, which='minor', linestyle='-', alpha=0.3)
    plt.tight_layout()
    
    if save_fig:
        fig.savefig("{}{}{}".format(save_fig['local'], 'electrical_condutivity', save_fig['tipo']))