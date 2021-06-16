import sys
from PyQt5 import QtWidgets

from window.PlotWindow import PlotWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    mainWin = PlotWindow()    
    mainWin.show()
    
    sys.exit( app.exec_() )