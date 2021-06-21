import sys
from PyQt5 import QtWidgets

from app.app import Ui

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--pontos', help="Número de pontos por ciclo")
    # parser.add_argument('--ciclos', help="Número de ciclos")
    # parser.add_argument('--freq', help="Frequência")

    # args = parser.parse_args()

    # pontos = int(args.pontos) if args.pontos else 100
    # ciclos = int(args.ciclos) if args.ciclos else 1
    # freq = int(args.freq) if args.freq else 60
    
    # main(pontos=pontos, ciclos=ciclos, freq=freq)