from PyQt6 import QtCore, QtWidgets


class gui_MicroVuProcessorMainWindow(object):
    def setupUi(self, MicroVuProcessorMainWindow):

        MicroVuProcessorMainWindow.setObjectName("MicroVuProcessorMainWindow")
        MicroVuProcessorMainWindow.resize(800, 490)
        MicroVuProcessorMainWindow.setMinimumSize(QtCore.QSize(800, 490))
        MicroVuProcessorMainWindow.setMaximumSize(QtCore.QSize(800, 490))
        MicroVuProcessorMainWindow.setWindowTitle("MicroVu 1Factory Processor")

        self.centralwidget = QtWidgets.QWidget(parent=MicroVuProcessorMainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.chkSelectAll = QtWidgets.QCheckBox(self.centralwidget)
        self.chkSelectAll.setVisible(False)
        self.chkSelectAll.setChecked(True)
        self.chkSelectAll.setGeometry(QtCore.QRect(660, 150, 70, 17))
        self.chkSelectAll.setText("")
        self.chkSelectAll.setObjectName("chkSelectAll")

        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 761, 120))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.output_label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.output_label.setObjectName("output_label")
        self.output_label.setText("Output Folder:  ")
        self.gridLayout.addWidget(self.output_label, 0, 0, 1, 1)

        self.txtOutputFolder = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtOutputFolder.setObjectName("txtOutputFolder")
        self.txtOutputFolder.setReadOnly(True)
        self.gridLayout.addWidget(self.txtOutputFolder, 0, 2, 1, 1)

        self.btnSelectOutputFolder = QtWidgets.QToolButton(parent=self.gridLayoutWidget)
        self.btnSelectOutputFolder.setObjectName("btnSelectOutputFolder")
        self.btnSelectOutputFolder.setText("...")
        self.gridLayout.addWidget(self.btnSelectOutputFolder, 0, 3, 1, 1)

        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.label.setText("Input Folder:  ")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.txtInputFolder = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtInputFolder.setObjectName("txtInputFolder")
        self.txtInputFolder.setReadOnly(True)
        self.gridLayout.addWidget(self.txtInputFolder, 1, 2, 1, 1)

        self.btnSelectInputFolder = QtWidgets.QToolButton(parent=self.gridLayoutWidget)
        self.btnSelectInputFolder.setObjectName("btnSelectInputFolder")
        self.btnSelectInputFolder.setText("...")
        self.gridLayout.addWidget(self.btnSelectInputFolder, 1, 3, 1, 1)

        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Initials:  ")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtInitials = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtInitials.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txtInitials.setObjectName("txtInitials")
        self.gridLayout.addWidget(self.txtInitials, 2, 2, 1, 1)

        self.OpNumberLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.OpNumberLabel.setObjectName("OpNumberLabel")
        self.OpNumberLabel.setText("Op Number:")
        self.gridLayout.addWidget(self.OpNumberLabel, 3, 0, 1, 1)
        self.txtOpNumber = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtOpNumber.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txtOpNumber.setObjectName("txtOpNumber")
        self.gridLayout.addWidget(self.txtOpNumber, 3, 2, 1, 1)

        self.LabelRevNumber = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.LabelRevNumber.setObjectName("LabelRevNumber")
        self.LabelRevNumber.setText("Rev:")
        self.gridLayout.addWidget(self.LabelRevNumber, 4, 0, 1, 1)
        self.txtRevNumber = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtRevNumber.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txtRevNumber.setObjectName("txtRevNumber")
        self.gridLayout.addWidget(self.txtRevNumber, 4, 2, 1, 1)

        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 180, 760, 238))
        self.tableWidget.setMinimumSize(QtCore.QSize(760, 238))
        self.tableWidget.setMaximumSize(QtCore.QSize(760, 238))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnWidth(0, 270)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 270)
        self.tableWidget.setColumnWidth(3, 100)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.setVisible(False)

        self.btnProcessFiles = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnProcessFiles.setGeometry(QtCore.QRect(680, 430, 100, 23))
        self.btnProcessFiles.setEnabled(False)
        self.btnProcessFiles.setObjectName("btnProcessFiles")
        self.btnProcessFiles.setText("Execute")

        MicroVuProcessorMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MicroVuProcessorMainWindow)
        self.statusbar.setObjectName("statusbar")
        MicroVuProcessorMainWindow.setStatusBar(self.statusbar)



