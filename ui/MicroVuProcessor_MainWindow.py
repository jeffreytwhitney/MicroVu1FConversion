import os
import sys
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from pathlib import Path

import lib.Utilities
import lib.MicroVuFileProcessor
from lib.MicroVuFileProcessor import ProcessorException
from ui.gui_MicroVuProcessor_MainWindow import gui_MicroVuProcessorMainWindow
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt


class MicroVuProcessorMainWindow(QtWidgets.QMainWindow, gui_MicroVuProcessorMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSelectInputFolder.clicked.connect(self.btnSelectInputFolder_clicked)
        self.btnSelectOutputFolder.clicked.connect(self.btnSelectOutputFolder_clicked)
        self.btnProcessFiles.clicked.connect(self.btnProcessFiles_clicked)
        self.user_initials = lib.Utilities.GetStoredIniValue("UserSettings", "Initials", "Settings")
        self.input_rootpath = lib.Utilities.GetStoredIniValue("Paths", "InputRootpath", "Settings")
        self.output_rootpath = lib.Utilities.GetStoredIniValue("Paths", "OutputRootpath", "Settings")
        self.txtOutputFolder.setText(self.output_rootpath)
        self.txtInitials.setText(self.user_initials)

    def btnSelectInputFolder_clicked(self):
        input_folder = self.get_directory_via_dialog("Select Input Folder", self.input_rootpath)
        self.txtInputFolder.setText(input_folder)
        self.enable_process_button()

    def btnSelectOutputFolder_clicked(self):
        output_folder = self.get_directory_via_dialog("Select Output Folder", self.output_rootpath)
        self.txtOutputFolder.setText(output_folder)
        self.enable_process_button()

    def btnProcessFiles_clicked(self):
        if len(self.txtOpNumber.text()) == 0:
            self.show_error_message("Op Number field is blank.", "Error")
            return
        if len(self.txtInitials.text()) == 0:
            self.show_error_message("Initials field is blank.", "Error")
            return
        if len(self.txtInputFolder.text()) == 0:
            self.show_error_message("Input Folder field is blank.", "Error")
            return
        if len(self.txtOutputFolder.text()) == 0:
            self.show_error_message("Output Folder field is blank.", "Error")
            return
        if len(self.txtRevNumber.text()) == 0:
            self.show_error_message("Rev Number field is blank.", "Error")
            return
        lib.Utilities.StoreIniValue(self.txtInitials.text(), "UserSettings", "Initials", "Settings")
        lib.Utilities.StoreIniValue(self.txtOutputFolder.text(), "Paths", "OutputRootpath", "Settings")
        self.process_files()

    def load_files(self):
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.verticalHeader().setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MicroVuProcessorMainWindow", "MicroVuName"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MicroVuProcessorMainWindow", "IsProfile"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MicroVuProcessorMainWindow", "Process File"))
        if not os.path.exists(self.txtInputFolder.text()):
            self.show_error_message("Input directory doesn't exist.", "Error")
            return
        else:
            files = [fn for fn in os.listdir(self.txtInputFolder.text()) if fn.endswith('.iwp')]
            if not files:
                self.show_error_message("No files found", "Error")
                return
            self.tableWidget.setRowCount(len(files))
            for row, file in enumerate(files):
                textItem = QTableWidgetItem(file)
                textItem.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(row, 0, textItem)
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                chkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidget.setItem(row, 1, chkBoxItem)
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                chkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.CheckState.Checked)
                self.tableWidget.setItem(row, 2, chkBoxItem)
            self.tableWidget.setVisible(True)

    def enable_process_button(self):
        if len(self.txtOutputFolder.text()) > 0 and len(self.txtInputFolder.text()) > 0:
            self.load_files()
            self.btnProcessFiles.setEnabled(True)
        else:
            self.btnProcessFiles.setEnabled(False)

    def show_error_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def show_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def get_directory_via_dialog(self, title, default_directory=""):
        dialog = QFileDialog()
        return_path = dialog.getExistingDirectory(self, title, default_directory)
        return str(Path(return_path).absolute()) + "\\"

    def process_files(self):
        input_directory = self.txtInputFolder.text()
        directory_parts = input_directory.split("\\")
        input_subdirectory = directory_parts[-2] if directory_parts[-1] == "" else directory_parts[-1]
        output_directory = os.path.join(self.txtOutputFolder.text(), input_subdirectory)
        op_number = self.txtOpNumber.text()
        for row in range(self.tableWidget.rowCount()):
            checkbox = self.tableWidget.item(row, 2)
            process_file = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            if not process_file:
                continue
            file_name = self.tableWidget.item(row, 0).text()
            input_filepath = str(os.path.join(input_directory, file_name))
            output_filepath = str(os.path.join(str(output_directory), file_name))
            user_initials = self.txtInitials.text()
            checkbox = self.tableWidget.item(row, 1)
            rev_number = self.txtRevNumber.text()
            is_profile = (
                checkbox is not None
                and checkbox.checkState() == Qt.CheckState.Checked
            )
            file_processor = lib.MicroVuFileProcessor.get_processor(input_filepath, op_number, user_initials, output_filepath, rev_number, is_profile)
            try:
                file_processor.process_file()
            except ProcessorException as e:
                error_message = e.args[0]
                self.show_error_message(error_message, "Processing Error")
                continue
        self.show_message("Done!", "Done!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MicroVuProcessorMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
