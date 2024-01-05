import os
import sys
from pathlib import Path

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem

import lib.Utilities
from lib import MicroVuProgram, MicroVuFileProcessor
from lib.MicroVuFileProcessor import ProcessorException
from ui.gui_MicroVuProcessor_MainWindow import gui_MicroVuProcessorMainWindow


class MicroVuProcessorMainWindow(QtWidgets.QMainWindow, gui_MicroVuProcessorMainWindow):

    # Dunder Methods
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSelectInputFolder.clicked.connect(self._btnSelectInputFolder_clicked)
        self.btnProcessFiles.clicked.connect(self._btnProcessFiles_clicked)
        self.tableWidget.cellDoubleClicked.connect(self._table_item_doubleclicked)
        self.user_initials = lib.Utilities.GetStoredIniValue("UserSettings", "Initials", "Settings")
        self.input_rootpath = lib.Utilities.GetStoredIniValue("Paths", "Input_Rootpath", "Settings")
        self.output_rootpath = lib.Utilities.GetStoredIniValue("Paths", "Output_Rootpath", "Settings")
        self.smart_profile_directory = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_directory", "Settings")
        self.txtInitials.setText(self.user_initials)

    # Internal Methods
    def _show_error_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _show_message(self, message: str, title: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _get_user_response(self, message: str, title: str) -> QMessageBox.StandardButton:
        return QMessageBox.critical(self, title, message, QMessageBox.StandardButton.Yes
                                    | QMessageBox.StandardButton.No
                                    | QMessageBox.StandardButton.YesToAll)

    # Event Methods
    def _btnProcessFiles_clicked(self):
        if not self.is_form_valid():
            return
        for row in range(self.tableWidget.rowCount()):
            smartprofile_file_name = self.tableWidget.item(row, 2).text()
            checkbox = self.tableWidget.item(row, 1)
            is_profile = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            if is_profile and len(smartprofile_file_name) == 0:
                self._show_error_message("You need to enter a SmartProfile File Name.", "Missing Information")
                return

        lib.Utilities.StoreIniValue(self.txtInitials.text(), "UserSettings", "Initials", "Settings")
        self.process_files()

    def _btnSelectInputFolder_clicked(self):
        input_folder = self.get_directory_via_dialog("Select Input Folder", self.input_rootpath)
        self.txtInputFolder.setText(input_folder)
        self.enable_process_button()

    def _table_item_doubleclicked(self, row, column):

        self._show_message(f"{row}", "Hi")

    # Public Methods
    def clear_form(self):
        self.txtInputFolder.setText("")
        self.txtOpNumber.setText("")
        self.txtRevNumber.setText("")
        self.tableWidget.setRowCount(0)

    def enable_process_button(self):
        if len(self.txtInputFolder.text()) > 0:
            self.load_files()
            self.btnProcessFiles.setEnabled(True)
        else:
            self.btnProcessFiles.setEnabled(False)

    def get_directory_via_dialog(self, title, default_directory=""):
        dialog = QFileDialog()
        return_path = dialog.getExistingDirectory(self, title, default_directory)
        return str(Path(return_path).absolute()) + "\\"

    def _get_filepath_via_dialog(self, title: str, file_type: str, default_directory: str) -> str:
        dialog = QFileDialog()
        return dialog.getOpenFileName(self, title, default_directory, file_type)

    def is_form_valid(self) -> bool:
        if len(self.txtOpNumber.text()) == 0:
            self._show_error_message("Op Number field is blank.", "Error")
            return False
        if len(self.txtInitials.text()) == 0:
            self._show_error_message("Initials field is blank.", "Error")
            return False
        if len(self.txtInputFolder.text()) == 0:
            self._show_error_message("Input Folder field is blank.", "Error")
            return False
        if len(self.txtRevNumber.text()) == 0:
            self._show_error_message("Rev Number field is blank.", "Error")
            return False
        return True

    def load_files(self) -> None:
        self.tableWidget.setRowCount(1)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.verticalHeader().setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MicroVuProcessorMainWindow", "MicroVuName"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MicroVuProcessorMainWindow", "IsProfile"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MicroVuProcessorMainWindow", "SmartProfile FileName"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MicroVuProcessorMainWindow", "Process File"))

        if not os.path.exists(self.txtInputFolder.text()):
            self._show_error_message("Input directory doesn't exist.", "Error")
            return
        else:
            files = [fn for fn in os.listdir(self.txtInputFolder.text()) if fn.endswith('.iwp')]
            if not files:
                self._show_error_message("No files found", "Error")
                return
            self.tableWidget.setRowCount(len(files))
            for row, file in enumerate(files):
                textItem = QTableWidgetItem(file)
                textItem.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(row, 0, textItem)
                sp_textItem = QTableWidgetItem("")
                self.tableWidget.setItem(row, 2, sp_textItem)
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                chkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidget.setItem(row, 1, chkBoxItem)
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                chkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.CheckState.Checked)
                self.tableWidget.setItem(row, 3, chkBoxItem)
            self.tableWidget.setVisible(True)

    def load_microvu_program_list(self, input_directory: str, op_number: str, rev_number: str) -> list[MicroVuProgram]:
        micro_vus: list[MicroVuProgram] = []
        user_replied_yes_to_all: bool = False

        for row in range(self.tableWidget.rowCount()):
            checkbox = self.tableWidget.item(row, 3)
            process_file = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            if not process_file:
                continue

            file_name = self.tableWidget.item(row, 0).text()
            input_filepath = str(os.path.join(input_directory, file_name))
            smartprofile_file_name = self.tableWidget.item(row, 2).text()
            micro_vu = MicroVuProgram.MicroVuProgram(input_filepath, op_number, rev_number, smartprofile_file_name)

            checkbox = self.tableWidget.item(row, 1)
            user_entered_is_profile = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            if micro_vu.is_smartprofile and not user_entered_is_profile:
                self._show_error_message(f"File '{file_name}' is a SmartProfile program. You need to check the 'IsProfile' checkbox and add the name of the SmartProfile project.", "Invalid Entry")
                return []
            if user_entered_is_profile and not micro_vu.is_smartprofile:
                self._show_error_message(f"File '{file_name}' was designated as a SmartProfile program. It is not one.", "Invalid Entry")
                return []
            if not micro_vu.can_write_to_output_file:
                self._show_error_message(f"File '{file_name}' already exists in the output folder.", "Invalid Entry")
                return []
            if not user_replied_yes_to_all and micro_vu.has_calculators:
                user_reply = self._get_user_response(f"File '{file_name}' has calculators in it. Do you wish to continue processing?", "Do you wish to continue?")
                if user_reply == QMessageBox.StandardButton.No:
                    return []
                if user_reply == QMessageBox.StandardButton.YesToAll:
                    user_replied_yes_to_all = True
            micro_vus.append(micro_vu)
        return micro_vus

    def process_files(self):
        input_directory = self.txtInputFolder.text()
        op_number = self.txtOpNumber.text()
        rev_number = self.txtRevNumber.text()
        user_initials = self.txtInitials.text()
        micro_vus: list[MicroVuProgram] = self.load_microvu_program_list(input_directory, op_number, rev_number)
        if not micro_vus:
            return
        processor = MicroVuFileProcessor.get_processor(user_initials)
        for micro_vu in micro_vus:
            processor.add_micro_vu_program(micro_vu)
        try:
            processor.process_files()
        except ProcessorException as e:
            self._show_error_message(e.args[0], "Processing Error")
            return
        self.clear_form()
        self._show_message("Done!", "Done!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MicroVuProcessorMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
