# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:43:57 2020

@author: Rodolfo
"""

import numpy as np

#=============================================================================
# g(T)
#=============================================================================
def g_t(temp, coef: list, divisorTemp: float = 1):
    """
    g(T1) = a_0 + a_1*(T1**1) + a_2*(T1**2) + ... + a_9*(T1**9),
    T1    = temp/divisorTemp
    
    Parameters:
        temp : list or float
            List or number of temperature

        coef : list
            list of coefficients

        divisorTemp : float, optional
            Factor that divides temperature. The default is 1.

    Returns:
        list or float
            Return a list or a number with g(t) for all temperatures passed.

    """
    if type(temp) == float:
        g_tmp = 0
        for j in range(0, len(coef)):
            g_tmp = g_tmp + float(coef[j]) * ((1/(temp/divisorTemp))**j)  
        return g_tmp
    else:
        g = []

        for t in temp:
            g_tmp = 0
            for j in range(0, len(coef)):
                g_tmp = g_tmp + float(coef[j]) / np.power(t/divisorTemp, j)
            g.append(g_tmp)
    
        return g

#=============================================================================
# f(T)
#=============================================================================
def f_t(temp, coef: list, divisorTemp: float = 1000):
    """
    f(T1) = exp(a_0 + a_1*(T1**1) + a_2*(T1**2) + ... + a_9*(T1**9)),
    T1    = temp/divisorTemp

    Parameters:
        temp : list or float
            List or number of temperature

        coef : list
            list of coefficients

        divisorTemp : float, optional
            Factor that divides temperature. The default is 1.

    Returns:
        list or float
            Return a list or a number with f(t) for all temperatures passed.

    """
    if type(temp) == float:
        f_tmp = 0
        for j in range(0, len(coef)):
            f_tmp = f_tmp + float(coef[j]) * ((temp/divisorTemp)**j)  
        return np.exp(f_tmp)
    else:
        f = []

        for t in temp:
            f_tmp = 0
            for j in range(0, len(coef)):
                f_tmp = f_tmp + float(coef[j]) * np.power(t/divisorTemp,j)   
            f.append(np.exp(f_tmp))
    
        return f

#=============================================================================
# Density
#=============================================================================
def getDensity(temperature, coefs):
    """ 
    This function obtains the piecewise function of specific heat of the air
  
    Parameters: 
        temperature (list): list of temperatures
        coefs       (list): list of coefficients
  
    Returns: 
        list: returns the piecewise function of the specific heat
    """
    conds = [ (temperature >= 300) & (temperature <= 3000), 
              (temperature > 3000) & (temperature <= 30000)]
    
    funcs = [ lambda temperature: g_t(temperature, coefs['300-3000'], 1000),
              lambda temperature: f_t(temperature, coefs['3000-30000'], 1000)]
    
    temperature = [float(i) for i in temperature]    
    return np.piecewise(temperature, conds, funcs)

#=============================================================================
# Specific Heat
#=============================================================================
def getSpecificHeat(temperature, coefs):
    """ 
    This function obtains the piecewise function of specific heat of the air
  
    Parameters: 
        temperature (list): list of temperatures
        coefs       (list): list of coefficients
  
    Returns: 
        list: returns the piecewise function of the specific heat
    """
    conds = [ (temperature >= 300)   & (temperature < 6000), 
              (temperature >= 6000)  & (temperature < 15000), 
              (temperature >= 14800) & (temperature <= 30000)]
    
    funcs = [ lambda temperature: f_t(temperature, coefs['300-6000'], 1000),
              lambda temperature: f_t(temperature, coefs['6000-15000'], 1000),
              lambda temperature: f_t(temperature, coefs['15000-30000'], 1000)]
    
    temperature = [float(i) for i in temperature]  
    return np.piecewise(temperature, conds, funcs)

#=============================================================================
# Electrical Condutivity
#=============================================================================
def getElectricalCondutivity(temperature, coefs):
    """ 
    This function obtains the piecewise function of specific heat of the air
  
    Parameters: 
        temperature (list): list of temperatures
        coefs       (list): list of coefficients
  
    Returns: 
        list: returns the piecewise function of the specific heat
    """
    conds = [ (temperature >= 5000)  & (temperature < 30000)]
    
    funcs = [ lambda temperature: f_t(temperature, coefs['5000-30000'], 1000)]
    
    temperature = [float(i) for i in temperature]    
    return np.piecewise(temperature, conds, funcs)

#=============================================================================
# Viscosity
#=============================================================================
def getViscosity(temperature, coefs):
    """ 
    This function obtains the piecewise function of specific heat of the air
  
    Parameters: 
        temperature (list): list of temperatures
        coefs       (list): list of coefficients
  
    Returns: 
        list: returns the piecewise function of the specific heat
    """
    conds = [ (temperature >= 3000)  & (temperature < 30000)]
    
    funcs = [ lambda temperature: f_t(temperature, coefs['3000-30000'], 1000)]
    
    temperature = [float(i) for i in temperature]    
    return np.piecewise(temperature, conds, funcs)

#=============================================================================
# Thermal Condutivity
#=============================================================================
def getThermalCondutivity(temperature, coefs):
    """ 
    This function obtains the piecewise function of specific heat of the air
  
    Parameters: 
        temperature (list): list of temperatures
        coefs       (list): list of coefficients
  
    Returns: 
        list: returns the piecewise function of the specific heat
    """
    conds = [ (temperature >= 300)   & (temperature < 6000), 
              (temperature >= 6000)  & (temperature < 15000), 
              (temperature >= 15000) & (temperature <= 30000)]
    
    c1 = coefs['300-6000']
    c2 = coefs['6000-15000']
    c3 = coefs['15000-30000']
    
    funcs = [ lambda temperature: f_t(temperature, c1, 1000),
              lambda temperature: f_t(temperature, c2, 1000),
              lambda temperature: f_t(temperature, c3, 1000)]

    temperature = [float(i) for i in temperature] 
    return np.piecewise(temperature, conds, funcs)    