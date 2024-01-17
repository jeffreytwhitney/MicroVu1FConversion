import sys

from PyQt6 import QtCore, QtWidgets

import lib.Utilities
from lib.MicroVuProgram import MicroVuProgram
from ui.DimensionNameEntryDialog import DimensionNameEntryDialog


class Ui_OpenDialog(QtWidgets.QMainWindow):
    def setupUi(self, OpenDialog):
        OpenDialog.setObjectName("OpenDialog")
        OpenDialog.setWindowTitle("Open Dialog")
        OpenDialog.resize(550, 283)
        self.centralwidget = QtWidgets.QWidget(parent=OpenDialog)
        self.centralwidget.setObjectName("centralwidget")
        self.btnOpenDialog = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnOpenDialog.setGeometry(QtCore.QRect(220, 110, 91, 23))
        self.btnOpenDialog.setObjectName("btnOpenDialog")
        self.btnOpenDialog.setText("Open Dialog")
        self.btnOpenDialog.clicked.connect(self._btnOpenDialog_clicked)
        OpenDialog.setCentralWidget(self.centralwidget)

    def _btnOpenDialog_clicked(self):
        micro_vu = MicroVuProgram("C:\\TEST\\MVConversion\\Input\\311\\Pacing\\ANOKA_123456_REV A\\110045615_OP20_AA2_VMM_REV2.iwp", "10", "G", "")
        dialog = DimensionNameEntryDialog(self, micro_vu)
        result = dialog.exec()
        dim_names = dialog.manual_dimension_names

        for n in dim_names:
            print(n.name)


if __name__ == "__main__":
    stylesheet_filepath = lib.Utilities.get_filepath_by_name("../MacOS.qss")
    styleSheet = lib.Utilities.get_file_as_string(stylesheet_filepath)
    app = QtWidgets.QApplication(sys.argv)
    OpenDialog = QtWidgets.QMainWindow()
    ui = Ui_OpenDialog()
    ui.setupUi(OpenDialog)
    OpenDialog.show()
    sys.exit(app.exec())
