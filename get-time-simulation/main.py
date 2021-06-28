import os
import time
import pandas as pd
import plotly.express as px
import re
from pprint import pprint

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__() 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Transcript Files (*.trn);;All Files (*)", options=options)
        if fileName:
            print(get_time_from_file(fileName))       


def get_time_from_file(path):
    filename, extension = os.path.splitext(path)
    
    pattern_seconds = re.compile("t_sec:\s([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\ss")
    pattern_minutes = re.compile("t_min:\s([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\smin")
    pattern_hour    = re.compile("t_h:\s+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\sh")
    
    t_sec = list()
    t_min = list()
    t_h   = list()

    for i, line in enumerate(open(path)):
        check_pattern(pattern_seconds, line, t_sec)
        check_pattern(pattern_minutes, line, t_min)
        check_pattern(pattern_hour, line, t_h)

    columns = ['t_sec', 't_min', 't_h']

    df = pd.DataFrame(list(zip(t_sec, t_min, t_h)), columns=columns)
    # print(f"Total seconds: {sum(t_sec)}")
    # print(f"Total minutes: {sum(t_min)}")
    # print(f"Total hours: {sum(t_h)}")
    
    print("Total")
    print(df.sum())

    print("\nMédia")
    print(df.mean())

    print("Fim")
    
def check_pattern(pattern: str, line: str, lista: list):
    for match in re.finditer(pattern, line):
        lista.append(float(match.group().strip().split()[-2]))


if __name__ == '__main__':

    diretorio = os.path.dirname(__file__)
    path = os.path.join(diretorio, "_HOA_4.16kV_Malha_01_300_pontos_init.trn")
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


    get_time_from_file(path=path)