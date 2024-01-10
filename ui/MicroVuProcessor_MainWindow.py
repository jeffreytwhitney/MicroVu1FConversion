import os
import sys
from pathlib import Path

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem

import lib.Utilities
from lib.MicroVuFileProcessor import ProcessorException, get_processor
from lib.MicroVuProgram import MicroVuProgram
from ui.gui_MicroVuProcessor_MainWindow import gui_MicroVuProcessorMainWindow


class TableWrapperRow:
    micro_vu_name: str
    is_profile: bool
    smartprofile_filename: str
    process_file: bool


class TableWrapper:
    _table_widget: QtWidgets.QTableWidget
    _rows: list[TableWrapperRow]

    def __init__(self, table_widget: QtWidgets.QTableWidget):
        self._table_widget = table_widget
        self._load_rows()

    def _load_rows(self):
        self._rows = []
        for table_row in range(self._table_widget.rowCount()):
            wrapper_row = TableWrapperRow()

            wrapper_row.micro_vu_name = self._table_widget.item(table_row, 0).text()

            checkbox = self._table_widget.item(table_row, 1)
            wrapper_row.is_profile = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )

            wrapper_row.smartprofile_filename = self._table_widget.item(table_row, 2).text()

            checkbox = self._table_widget.item(table_row, 3)
            wrapper_row.process_file = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            self._rows.append(wrapper_row)

    @property
    def rows(self) -> list[TableWrapperRow]:
        return self._rows


class MicroVuProcessorMainWindow(QtWidgets.QMainWindow, gui_MicroVuProcessorMainWindow):
    _micro_vus: list[MicroVuProgram] = []

    # Dunder Methods
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSelectInputFolder.clicked.connect(self._btnSelectInputFolder_clicked)
        self.btnSelectOutputFolder.clicked.connect(self._btnSelectOutputFolder_clicked)
        self.btnProcessFiles.clicked.connect(self._btnProcessFiles_clicked)
        self.tableWidget.cellDoubleClicked.connect(self._table_item_doubleclicked)
        self.chkSelectAll.stateChanged.connect(self._chkSelectAll_stateChanged)
        self.user_initials = lib.Utilities.GetStoredIniValue("UserSettings", "Initials", "Settings")
        self.input_rootpath = lib.Utilities.GetStoredIniValue("Paths", "Input_Rootpath", "Settings")
        self.output_rootpath = lib.Utilities.GetStoredIniValue("Paths", "Output_Rootpath", "Settings")
        self.smart_profile_directory = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_directory", "Settings")
        self.txtInitials.setText(self.user_initials)
        self.txtOutputFolder.setText(self.output_rootpath)

    # Internal Methods
    def _get_directory_via_dialog(self, title, default_directory=""):
        dialog = QFileDialog()
        return_path = dialog.getExistingDirectory(self, title, default_directory)
        return "" if return_path == "" else str(Path(return_path).absolute()) + "\\"

    def _get_filepath_via_dialog(self, title: str, file_type: str, default_directory: str) -> str:
        dialog = QFileDialog()
        return dialog.getOpenFileName(self, title, default_directory, file_type)

    def _get_user_response(self, message: str, title: str) -> QMessageBox.StandardButton:
        return QMessageBox.critical(self, title, message, QMessageBox.StandardButton.Yes
                                    | QMessageBox.StandardButton.No
                                    | QMessageBox.StandardButton.YesToAll)

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

    # Event Methods
    def _chkSelectAll_stateChanged(self):
        checkstate = self.chkSelectAll.checkState()
        self.set_process_checkboxes_checkstate(checkstate)

    def _btnProcessFiles_clicked(self):
        if not self.is_form_valid:
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
        lib.Utilities.StoreIniValue(self.txtOutputFolder.text(), "Paths", "output_rootpath", "Settings")
        self.process_files()

    def _btnSelectInputFolder_clicked(self):
        input_folder = self._get_directory_via_dialog("Select Input Folder", self.input_rootpath)
        self.txtInputFolder.setText(input_folder)
        self.enable_process_button()

    def _btnSelectOutputFolder_clicked(self):
        output_folder = self._get_directory_via_dialog("Select Output Folder", self.output_rootpath)
        self.txtOutputFolder.setText(output_folder)
        self.enable_process_button()

    def _table_item_doubleclicked(self, row, column):
        if column != 2:
            return
        if user_result := self._get_filepath_via_dialog(
                "Select a SmartProfile file",
                "Smart Profile Files (*.spp)",
                self.smart_profile_directory,
        ):
            smartprofile_filepath = user_result[0]
            smartprofile_filename = Path(smartprofile_filepath).name
            self.tableWidget.item(row, column).setText(smartprofile_filename)
        else:
            return

    # Public Properties
    @property
    def calculator_micro_vu_warning(self) -> str:
        if not (calculator_micro_vus := self.micro_vus_with_calculators):
            return ""
        return_message: str = "The following programs have calculators in them:\r\n"
        for micro_vu in calculator_micro_vus:
            return_message += f"{micro_vu.filename}\r\n"
        return return_message.strip()

    @property
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

    @property
    def input_directory(self) -> str:
        return self.txtInputFolder.text()

    @property
    def micro_vus(self) -> list[MicroVuProgram]:
        return self._micro_vus

    @property
    def micro_vus_with_calculators(self) -> list[MicroVuProgram]:
        return [m for m in self.micro_vus if m.has_calculators]

    @property
    def op_number(self) -> str:
        return self.txtOpNumber.text()

    @property
    def rev_number(self) -> str:
        return self.txtRevNumber.text()

    @property
    def user_initials(self) -> str:
        return self.txtInitials.text()

    @user_initials.setter
    def user_initials(self, value):
        self.txtInitials.setText(value)

    # Public Methods
    def check_micro_vus_for_calculators(self, micro_vus: list[MicroVuProgram]) -> bool:
        if not micro_vus:
            return False

        for micro_vu in self.micro_vus_with_calculators:
            user_reply = self._get_user_response(f"File '{micro_vu.filename}' has calculators in it. Do you wish to continue processing?", "Do you wish to continue?")
            if user_reply == QMessageBox.StandardButton.No:
                return False
            if user_reply == QMessageBox.StandardButton.YesToAll:
                return True
        return True

    def clear_form(self):
        self.txtInputFolder.setText("")
        self.txtOpNumber.setText("")
        self.txtRevNumber.setText("")
        self.tableWidget.setRowCount(0)
        self._micro_vus.clear()

    def set_process_checkboxes_checkstate(self, check_state: Qt.CheckState) -> None:
        for table_row in range(self.tableWidget.rowCount()):
            checkbox = self.tableWidget.item(table_row, 3)
            if checkbox is None:
                continue
            checkbox.setCheckState(check_state)

    def enable_process_button(self):
        if len(self.txtInputFolder.text()) > 0 and len(self.txtOutputFolder.text()) > 0 and len(self.txtInitials.text()) > 0:
            self.load_table_widget()
            self.btnProcessFiles.setEnabled(True)
        else:
            self.btnProcessFiles.setEnabled(False)
            self.tableWidget.setRowCount(0)

    def load_micro_vus(self) -> None:
        micro_vus: list[MicroVuProgram] = []

        for row in range(self.tableWidget.rowCount()):
            checkbox = self.tableWidget.item(row, 3)
            process_file = (
                    checkbox is not None
                    and checkbox.checkState() == Qt.CheckState.Checked
            )
            if not process_file:
                continue

            file_name = self.tableWidget.item(row, 0).text()
            input_filepath = str(os.path.join(self.input_directory, file_name))
            smartprofile_file_name = Path(self.tableWidget.item(row, 2).text()).stem
            micro_vu = MicroVuProgram(input_filepath, self.op_number, self.rev_number, smartprofile_file_name)
            micro_vus.append(micro_vu)
        self._micro_vus.clear()
        self._micro_vus = micro_vus

    def load_table_widget(self) -> None:
        self.tableWidget.setRowCount(1)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.verticalHeader().setVisible(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("MicroVuName")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("IsProfile")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("SmartProfile FileName")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText("Process File")

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
                self.tableWidget.setRowHeight(row, 20)
            self.chkSelectAll.setChecked(True)
            self.chkSelectAll.setVisible(True)
            self.setEnabled(True)
            self.tableWidget.setVisible(True)

    def process_files(self):
        self.load_micro_vus()
        if not self.micro_vus:
            return

        table_wrapper = TableWrapper(self.tableWidget)

        validator = self.MicroVuValidator(self.micro_vus, table_wrapper)
        if not validator.is_valid:
            self._show_error_message(validator.validation_message, "Invalid Entry")
            return

        if not self.check_micro_vus_for_calculators(self.micro_vus):
            return

        processor = get_processor(self.user_initials)
        processor.add_micro_vu_programs(self.micro_vus)

        try:
            processor.process_files()
        except ProcessorException as e:
            self._show_error_message(e.args[0], "Processing Error")
            return

        if not self.micro_vus_with_calculators:
            self._show_message("Done!", "Done!")
        else:
            self._show_message(self.calculator_micro_vu_warning, "Done!")
        self.clear_form()

    class MicroVuValidator:

        _micro_vus: list[MicroVuProgram]
        _table_wrapper: TableWrapper
        _is_valid: bool = False
        _validation_message: str = ""

        # Dunder Methods
        def __init__(self, micro_vus: list[MicroVuProgram], table_wrapper: TableWrapper):
            self._micro_vus = micro_vus
            self._table_wrapper = table_wrapper
            self._validate_micro_vus()

        # Internal Methods
        def _validate_micro_vus(self):
            validation_message: str = ""

            for row in self._table_wrapper.rows:
                if not row.process_file:
                    continue

                micro_vu = next((mv for mv in self._micro_vus if mv.filename == row.micro_vu_name), None)
                if not micro_vu:
                    continue

                if micro_vu.is_smartprofile and not row.is_profile:
                    validation_message += f"File '{row.micro_vu_name}' is a SmartProfile program. You need to check the 'IsProfile' checkbox and add the name of the SmartProfile project. \r\n"
                if row.is_profile and not micro_vu.is_smartprofile:
                    validation_message += f"File '{row.micro_vu_name}' was designated as a SmartProfile program. It is not one. \r\n"
                if not micro_vu.can_write_to_output_file:
                    validation_message += f"File '{row.micro_vu_name}' already exists in the output folder. \r\n"

            if not validation_message:
                self._is_valid = True
                self._validation_message = ""
            else:
                self._is_valid = False
                self._validation_message = f"Validation Messages:\r\n{validation_message.strip()}"

        # Properties
        @property
        def is_valid(self):
            return self._is_valid

        @property
        def validation_message(self):
            return self._validation_message


def main():
    stylesheet_filepath = lib.Utilities.get_filepath_by_name("MacOS.qss")
    styleSheet = lib.Utilities.get_file_as_string(stylesheet_filepath)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    ui = MicroVuProcessorMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
