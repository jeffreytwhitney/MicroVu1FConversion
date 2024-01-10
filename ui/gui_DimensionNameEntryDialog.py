from PyQt6 import QtCore, QtGui, QtWidgets


class gui_DimensionNameEntryDialog(object):
    _title: str

    def __init__(self):
        super().__init__()

    def set_form_title(self, value: str):
        self._title = value

    def setupUi(self, DimensionNameEntryDialog):
        DimensionNameEntryDialog.setWindowTitle("Enter Balloon Numbers")
        DimensionNameEntryDialog.setObjectName("DimensionNameEntryDialog")
        DimensionNameEntryDialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        DimensionNameEntryDialog.resize(700, 800)
        DimensionNameEntryDialog.setMinimumSize(QtCore.QSize(700, 800))
        DimensionNameEntryDialog.setMaximumSize(QtCore.QSize(700, 800))

        self.title_Label = QtWidgets.QLabel(parent=DimensionNameEntryDialog)
        self.title_Label.setText(self._title)
        self.title_Label.setGeometry(QtCore.QRect(10, 10, 700, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title_Label.setFont(font)
        self.title_Label.setObjectName("title_Label")

        self.warning_Label = QtWidgets.QLabel(parent=DimensionNameEntryDialog)
        self.warning_Label.setText("Enter Balloon number only. Example('10', '12A', '12B')")
        self.warning_Label.setGeometry(QtCore.QRect(10, 50, 700, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.warning_Label.setFont(font)
        self.warning_Label.setObjectName("warning_Label")

        self.dimensionTable = QtWidgets.QTableWidget(parent=DimensionNameEntryDialog)
        self.dimensionTable.setGeometry(QtCore.QRect(10, 80, 660, 681))
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

        self.btnOK = QtWidgets.QPushButton(parent=DimensionNameEntryDialog)
        self.btnOK.setGeometry(QtCore.QRect(570, 770, 100, 23))
        self.btnOK.setObjectName("btnOK")
        self.btnOK.setText("OK")

        self.btnCancel = QtWidgets.QPushButton(parent=DimensionNameEntryDialog)
        self.btnCancel.setGeometry(QtCore.QRect(465, 770, 100, 23))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")

