import sys
from PyQt6 import QtWidgets
from ui.MicroVuProcessor_MainWindow import MicroVuProcessorMainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MicroVuProcessorMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
