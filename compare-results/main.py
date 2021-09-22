import sys
import os
from PyQt5 import QtWidgets

from app2.app import Ui

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui(os.getcwd())                # Create an instance of our class
    app.exec_()                             # Start the application
