from typing import List

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QWidget

import lib.Utilities
from lib import MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram, DimensionName
from lib.MicroVuFileProcessor import Processor


class DimensionNameEntryDialog(QtWidgets.QDialog):
    _manual_dimension_names: List[DimensionName]
    _micro_vu: MicroVuProgram
    _processor: Processor

    # Dunder Methods
    def __init__(self, parent: QWidget, mv: MicroVuProgram):
        super().__init__()
        self.parent = parent
        self._micro_vu = mv
        self._manual_dimension_names = mv.dimension_names
        self._processor = MicroVuFileProcessor.get_processor("JTW")
        self._setupUi()
        self.btnAutoFill.clicked.connect(self._btnAutoFill_clicked)
        self.btnOK.clicked.connect(self._btnOK_clicked)
        self.btnCancel.clicked.connect(self._btnCancel_clicked)
        self.dimensionTable.keyPressEvent = self._tableKeyPressEvent
        self._load_form()

    # Event Methods
    def _btnAutoFill_clicked(self):
        for row, dimension_name in enumerate(self._manual_dimension_names):
            new_name = self._processor.parse_dimension_name(dimension_name.name, "")
            new_name_item = QTableWidgetItem(new_name)
            self.dimensionTable.setItem(row, 1, new_name_item)

    def _btnOK_clicked(self):
        if not self._validate_table():
            return
        self._update_manual_dimension_names()
        self.accept()

    def _btnCancel_clicked(self):
        self.reject()

    def _tableKeyPressEvent(self, event):
        # call the base implementation, do *not* use super()!
        QtWidgets.QTableWidget.keyPressEvent(self.dimensionTable, event)
        if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            current = self.dimensionTable.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.dimensionTable.setCurrentIndex(nextIndex)
                self.dimensionTable.edit(nextIndex)

    def _tableDoubleClicked(self, mi):
        row = mi.row()
        column = mi.column()
        if column > 0:
            return
        table_cell = self.dimensionTable.item(row, column)
        table_cell_value = table_cell.text()
        new_cell = self.dimensionTable.item(row, 1)
        new_cell.setText(table_cell_value)

    # Internal Methods
    def _get_user_response(self, message: str, title: str) -> QMessageBox.StandardButton:
        return QMessageBox.critical(self, title, message, QMessageBox.StandardButton.Yes
                                    | QMessageBox.StandardButton.No | QMessageBox.StandardButton.YesToAll)

    def _load_form(self):
        if not self._micro_vu:
            return
        if self._micro_vu.is_smartprofile:
            return
        if not self._manual_dimension_names:
            return

        self.dimensionTable.setRowCount(len(self._manual_dimension_names))
        self.dimensionTable.setSortingEnabled(False)
        self.dimensionTable.verticalHeader().setVisible(False)
        item = self.dimensionTable.horizontalHeaderItem(0)
        item.setText("Old Name")
        item = self.dimensionTable.horizontalHeaderItem(1)
        item.setText("New Name")

        for row, dimension_name in enumerate(self._manual_dimension_names):
            old_name_item = QTableWidgetItem(dimension_name.name)
            old_name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.dimensionTable.setItem(row, 0, old_name_item)
            new_name = self._processor.parse_dimension_name(dimension_name.name, "")
            new_name_item = QTableWidgetItem(new_name)
            self.dimensionTable.setItem(row, 1, new_name_item)
            self.dimensionTable.setRowHeight(row, 20)
        self.dimensionTable.doubleClicked.connect(self._tableDoubleClicked)
        self.dimensionTable.setVisible(True)

    def _reset_table_cells_color(self):
        for row, dimension_name in enumerate(range(self.dimensionTable.rowCount())):
            item = self.dimensionTable.item(row, 1)
            item.setBackground(QColor("#FFFFFF"))

    def _setupUi(self):
        self.setWindowTitle("Enter Balloon Numbers")
        self.setObjectName("DimensionNameEntryDialog")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(700, 800)
        self.setMinimumSize(QtCore.QSize(700, 800))
        self.setMaximumSize(QtCore.QSize(700, 800))

        self.title_Label = QtWidgets.QLabel(parent=self)
        self.title_Label.setText(self.form_title)
        self.title_Label.setGeometry(QtCore.QRect(10, 10, 700, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title_Label.setFont(font)
        self.title_Label.setObjectName("title_Label")

        self.warning_Label = QtWidgets.QLabel(parent=self)
        self.warning_Label.setText("Enter Balloon number only. Example('10', '12A', '12B')")
        self.warning_Label.setGeometry(QtCore.QRect(10, 50, 700, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.warning_Label.setFont(font)
        self.warning_Label.setObjectName("warning_Label")

        self.dimensionTable = QtWidgets.QTableWidget(parent=self)
        self.dimensionTable.setGeometry(QtCore.QRect(10, 120, 660, 621))
        self.dimensionTable.setObjectName("dimensionTable")
        self.dimensionTable.setColumnCount(2)
        self.dimensionTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.dimensionTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dimensionTable.setHorizontalHeaderItem(1, item)
        self.dimensionTable.horizontalHeaderItem(0).setText("Old_Name")
        self.dimensionTable.horizontalHeaderItem(1).setText("New_Name")
        self.dimensionTable.setColumnWidth(0, 150)
        self.dimensionTable.setColumnWidth(1, 150)
        self.btnOK = QtWidgets.QPushButton(parent=self)
        self.btnOK.setGeometry(QtCore.QRect(570, 770, 100, 23))
        self.btnOK.setObjectName("btnOK")
        self.btnOK.setText("OK")

        self.btnCancel = QtWidgets.QPushButton(parent=self)
        self.btnCancel.setGeometry(QtCore.QRect(465, 770, 100, 23))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")

        self.btnAutoFill = QtWidgets.QPushButton(parent=self)
        self.btnAutoFill.setGeometry(QtCore.QRect(190, 90, 100, 23))
        self.btnAutoFill.setObjectName("btnAutoFill")
        self.btnAutoFill.setText("AutoFill")

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

    def _update_manual_dimension_names(self):
        dimension_root = lib.Utilities.GetStoredIniValue("GlobalSettings", "dimension_root", "Settings")

        for row in range(self.dimensionTable.rowCount()):
            self.manual_dimension_names[row].name = dimension_root + self.dimensionTable.item(row, 1).text().upper()

    # Properties
    @property
    def form_title(self) -> str:
        program_name = self._micro_vu.filename
        return f"Enter Balloon Numbers for program \'{program_name}\':"

    @property
    def manual_dimension_names(self) -> List[DimensionName]:
        return self._manual_dimension_names
