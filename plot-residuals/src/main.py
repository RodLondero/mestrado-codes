import sys
from PyQt5 import QtWidgets

from gui.window import Ui


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    mainWin = Ui()    
    mainWin.show()
    
    sys.exit( app.exec_() )
    