import sys
from collections.abc import Callable
from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

import lib.Utilities
from lib.MicroVuProgram import MicroVuProgram, DimensionName
from ui.gui_DimensionNameEntryDialog import gui_DimensionNameEntryDialog


class DimensionNameEntryDialog(QtWidgets.QMainWindow, gui_DimensionNameEntryDialog):
    _manual_dimension_names: List[DimensionName]
    _micro_vu: MicroVuProgram
    _save_callback: Callable[MicroVuProgram]
    _cancel_callback: Callable[]

    # Dunder Methods
    def __init__(self, mv: MicroVuProgram):
        super().__init__()
        self._micro_vu = mv
        self._manual_dimension_names = mv.dimension_names
        self.set_form_title(self.form_title)
        self.setupUi(self)

    # Event Methods
    def _btnOK_clicked(self):
        if not self._validate_table():
            return
        self._micro_vu.manual_dimension_names = self._manual_dimension_names
        if callable(self._save_callback):
            self._save_callback(self._micro_vu)

    def _btnCancel_clicked(self):
        if callable(self._cancel_callback):
            self._cancel_callback()

    # Internal Methods
    def _get_user_response(self, message: str, title: str) -> QMessageBox.StandardButton:
        return QMessageBox.critical(self, title, message, QMessageBox.StandardButton.Yes
                                    | QMessageBox.StandardButton.No
                                    | QMessageBox.StandardButton.YesToAll)

    def _reset_table_cells_color(self):
        for row, dimension_name in enumerate(range(self.dimensionTable.rowCount())):
            item = self.dimensionTable.item(row, 1)
            item.setBackground(QColor("#FFFFFF"))

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

    def _update_dimension_names_from_table(self):
        for row, dimension_name in enumerate(range(self.dimensionTable.setRowCount)):
            self._manual_dimension_names[row].name = self.dimensionTable.item(row, 1).text()

    def _validate_table(self) -> bool:
        self._reset_table_cells_color()

        new_names: List[str] = [
                self.dimensionTable.item(row, 1).text()
                for row, dimension_name in enumerate(
                        range(self.dimensionTable.rowCount())
                )
        ]

        any_blanks = False
        for name in new_names:
            if len(name.strip()) == 0:
                any_blanks = True

        if any_blanks:
            for row, dimension_name in enumerate(range(self.dimensionTable.rowCount())):
                item = self.dimensionTable.item(row, 1)
                if item.text() == "":
                    item.setBackground(QColor().fromRgb(220, 20, 60, 60))
            self._show_error_message("You have to enter values for each balloon number.", "Missing Balloon Numbers")
            return False

        if dupes := [x for n, x in enumerate(new_names) if x in new_names[:n]]:
            for row, dimension_name in enumerate(range(self.dimensionTable.rowCount())):
                item = self.dimensionTable.item(row, 1)
                if item.text() in dupes:
                    item.setBackground(QColor().fromRgb(220, 20, 60, 60))
            self._show_error_message("You can't have duplicate balloon numbers.", "Duplicate Balloon Numbers")
            return False
        return True

    # Public Methods 
    def load_form(self):
        if not self._micro_vu:
            return
        if self._micro_vu.is_smartprofile:
            return
        if not self._manual_dimension_names:
            return

        self.btnOK.clicked.connect(self._btnOK_clicked)

        self.dimensionTable.setRowCount(len(self._manual_dimension_names))
        self.dimensionTable.setSortingEnabled(False)
        self.dimensionTable.verticalHeader().setVisible(False)
        item = self.dimensionTable.horizontalHeaderItem(0)
        item.setText("Old Name")
        item = self.dimensionTable.horizontalHeaderItem(1)
        item.setText("New Name")

        for row, dimension_name in enumerate(self._manual_dimension_names):
            old_name_item = QTableWidgetItem(dimension_name.name)
            old_name_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.dimensionTable.setItem(row, 0, old_name_item)
            new_name_item = QTableWidgetItem("")
            self.dimensionTable.setItem(row, 1, new_name_item)
            self.dimensionTable.setRowHeight(row, 20)
        self.dimensionTable.setVisible(True)

    def set_form_save_callback(self, func: Callable[MicroVuProgram]):
        _save_callback = func

    def form_cancelled(self, func: Callable):
        _cancel_callback = func

    # Properties
    @property
    def form_title(self) -> str:
        program_name = self._micro_vu.filename
        return f"Enter Balloon Numbers for program \'{program_name}\':"


if __name__ == "__main__":
    stylesheet_filepath = lib.Utilities.get_filepath_by_name("MacOS.qss")
    styleSheet = lib.Utilities.get_file_as_string(stylesheet_filepath)
    micro_vu = MicroVuProgram("C:\\TEST\\MVConversion\\Input\\311\\Pacing\\A_123456_REV2\\NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp", "10", "G", "")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    ManualDimensionNameEntry = QtWidgets.QDialog()
    ui = DimensionNameEntryDialog(micro_vu)
    ui.setupUi(ManualDimensionNameEntry)
    ui.load_form()
    ManualDimensionNameEntry.show()
    sys.exit(app.exec())
