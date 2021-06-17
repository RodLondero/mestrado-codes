import sys
from PyQt5.QtWidgets import QApplication
from core.window import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App(csv_decimal=".")
    sys.exit(app.exec_())
