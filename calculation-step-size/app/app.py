from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

import pandas as pd
import sys
import os
import csv
import plotly.express as px
import plotly.graph_objs as go
import pathlib

pathdir = pathlib.Path(__file__).parent.absolute()


class Ui(QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(f'{pathdir}/app.ui', self)  # Load the .ui file

        self.setFixedSize(300, 160)
        self.setMinimumSize(300, 160)
        # Edits
        self.spinBoxPontos = self.findChild(QSpinBox, 'spinBoxPontos')  # type: QSpinBox
        self.spinBoxPontos.setMaximum(10000)
        self.spinBoxCiclos = self.findChild(QSpinBox, 'spinBoxCiclos')  # type: QSpinBox
        self.editPassos    = self.findChild(QLineEdit, 'editPassos')    # type: QLineEdit
        self.editPasso     = self.findChild(QLineEdit, 'editPasso')     # type: QLineEdit

        # CheckBox
        self.checkBoxPlotar = self.findChild(QCheckBox, 'checkBoxPlotar') # type: QCheckBox

        # Button
        self.btnCalcular = self.findChild(QPushButton, 'btnCalcular')
        self.btnCalcular.clicked.connect(self.calcular)

        # Keyboard
        # self.spinBoxCiclos.returnPressed.connect(self)

        self.show()

    def calcular(self):

        pontos = int(self.spinBoxPontos.text())
        ciclos = int(self.spinBoxCiclos.text())
        freq = 60

        T = 1/freq
        w = 2 * np.pi * freq
        
        step = T / pontos
        
        # Tempo
        t = np.arange(0, ciclos*T, step)
        t_ms = t*1000

        self.editPasso.setText(f"{step:0.2e}")
        self.editPassos.setText(str(len(t)))

        print(f"Step: {step}")
        print(f"Steps: {len(t)}")

        if self.checkBoxPlotar.isChecked():
            # Senoide
            ia = 10e3*np.cos(w*t)
            ib = 10e3*np.cos(w*t - 2 * np.pi / 3)
            ic = 10e3*np.cos(w*t + 2 * np.pi / 3)

            # Figura
            # fig = plt.figure()  # type: fig.Figure
            # ax = fig.subplots(1) # type: axes.Axes
            
            # ax.plot(t_ms, ia, '.-', label='$I_A$')
            # ax.plot(t_ms, ib, '.-', label='$I_B$')
            # ax.plot(t_ms, ic, '.-', label='$I_C$')

            # titulo = "$\\bf{StepSize:}$ " + f"{step:.2g}" + " | " + "$\\bf{Pontos:}$ " + f"{pontos}"
            # ax.set_title(titulo)
            # # ax.set_title(f"&Step-Size&: {step:.4f} | Pontos: {pontos}")
            # ax.set_xlim(left=0, right=max(t_ms))
            # ax.set_ylim(bottom=min(ia), top=max(ia))
            
            # ax.set_xlabel("Tempo ($ms$)")
            # ax.set_ylabel("Amplitude")
            # ax.legend(loc='upper right')
            
            # ax.xaxis.set_major_locator(MultipleLocator(max(t_ms) / 10))
            # ax.xaxis.set_minor_locator(MultipleLocator(max(t_ms) / 10 / 2))
            
            # ax.yaxis.set_major_locator(MultipleLocator(2*max(ia) / 10))
            # ax.yaxis.set_minor_locator(MultipleLocator(2*max(ia) / 10 / 2))    
            
            # ax.grid(b=True, which='major', alpha=0.5, ls='solid')
            # ax.grid(b=True, which='minor', alpha=0.5, ls='dashed')

            # plt.tight_layout()
            # plt.show()    

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=t_ms, y=ia, mode='lines+markers'))
            fig2.add_trace(go.Scatter(x=t_ms, y=ib, mode='lines+markers'))
            fig2.add_trace(go.Scatter(x=t_ms, y=ic, mode='lines+markers'))
            fig2.update_layout(
                title=f"StepSize: {step:.2g}, Pontos: {pontos}"
            )
            fig2.show()

    def keyPressEvent(self, qKeyEvent):
        print(qKeyEvent.key())
        if qKeyEvent.key() == Qt.Key_Return: 
            self.calcular()
        else:
            super().keyPressEvent(qKeyEvent)