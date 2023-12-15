import sys

from PyQt6.QtWidgets import QMessageBox, QFileDialog
from pathlib import Path
from ui.gui_MicroVuProcessor_MainWindow import gui_MicroVuProcessorMainWindow
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt





class MicroVuProcessorMainWindow(QtWidgets.QMainWindow, gui_MicroVuProcessorMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSelectInputFolder.clicked.connect(self.btnSelectInputFolder_clicked)
        self.btnSelectOutputFolder.clicked.connect(self.btnSelectOutputFolder_clicked)
        self.btnProcessFiles.clicked.connect(self.btnProcessFiles_clicked)


    def btnSelectInputFolder_clicked(self):
        input_folder = self.get_directory_via_dialog("Select Input Folder", "V:\\Inspect Programs\\CMM Programs\\B_S Approved Programs\\PDF Approved Programs\\")
        self.txtInputFolder.setText(input_folder)
        self.enable_process_button()

    def btnSelectOutputFolder_clicked(self):
        outputfolder = self.get_directory_via_dialog("Select Output Folder", "")
        self.txtOutputFolder.setText(outputfolder)
        self.enable_process_button()

    def btnProcessFiles_clicked(self):
        pass

    def load_files(self, directory):
        pass

    def enable_process_button(self):
        jim = self.txtOutputFolder.text()
        if len(self.txtOutputFolder.text()) > 0 and len(self.txtInputFolder.text()) > 0:
            self.btnProcessFiles.setEnabled(True)
        else:
            self.btnProcessFiles.setEnabled(False)

    def show_error_message(self, message, title):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def get_directory_via_dialog(self, title, default_directory=""):
        dialog = QFileDialog()
        return_path = dialog.getExistingDirectory(self, title, default_directory)
        return str(Path(return_path).absolute()) + "\\"


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MicroVuProcessorMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()