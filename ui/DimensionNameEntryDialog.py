import sys
from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem

from lib.MicroVuProgram import MicroVuProgram, DimensionName
from ui.gui_DimensionNameEntryDialog import gui_DimensionNameEntryDialog


class DimensionNameEntryDialog(QtWidgets.QMainWindow, gui_DimensionNameEntryDialog):
    _manual_dimension_names: List[DimensionName]
    _micro_vu: MicroVuProgram

    # Dunder Methods
    def __init__(self, mv: MicroVuProgram):
        super().__init__()
        self._micro_vu = mv
        self._manual_dimension_names = mv.dimension_names
        self.set_form_title(self.form_title)
        self.setupUi(self)

    def load_table(self):
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
            old_name_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.dimensionTable.setItem(row, 0, old_name_item)
            new_name_item = QTableWidgetItem("")
            self.dimensionTable.setItem(row, 1, new_name_item)
            self.dimensionTable.setRowHeight(row, 20)
        self.dimensionTable.setVisible(True)

    def _update_dimension_names_from_table(self):
        for row, dimension_name in enumerate(range(self.dimensionTable.setRowCount)):
            self._manual_dimension_names[row].name = self.dimensionTable.item(row, 1).text()

    def _validate_table(self):
        new_names: List[str] = [
            self.dimensionTable.item(row, 1).text()
            for row, dimension_name in enumerate(
                range(self.dimensionTable.setRowCount)
            )
        ]
        dupes = [x for n, x in enumerate(new_names) if x in new_names[:n]]
        blanks = [x for x in new_names if x == ""]



    @property
    def form_title(self) -> str:
        program_name = self._micro_vu.filename
        return f"Enter Balloon Numbers for program \'{program_name}\':"


if __name__ == "__main__":
    micro_vu = MicroVuProgram("C:\\TEST\\MVConversion\\Input\\311\\Pacing\\A_123456_REV2\\NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp", "10", "G", "")
    app = QtWidgets.QApplication(sys.argv)
    ManualDimensionNameEntry = QtWidgets.QDialog()
    ui = DimensionNameEntryDialog(micro_vu)
    ui.setupUi(ManualDimensionNameEntry)
    ui.load_table()
    ManualDimensionNameEntry.show()
    sys.exit(app.exec())
