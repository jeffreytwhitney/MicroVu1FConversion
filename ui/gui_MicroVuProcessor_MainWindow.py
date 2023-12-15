from PyQt6 import QtCore, QtGui, QtWidgets


class gui_MicroVuProcessorMainWindow(object):
    def setupUi(self, MicroVuProcessorMainWindow):
        MicroVuProcessorMainWindow.setObjectName("MicroVuProcessorMainWindow")
        MicroVuProcessorMainWindow.resize(853, 415)
        self.centralwidget = QtWidgets.QWidget(parent=MicroVuProcessorMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 761, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtInputFolder = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtInputFolder.setObjectName("txtInputFolder")
        self.gridLayout.addWidget(self.txtInputFolder, 0, 2, 1, 1)
        self.btnSelectInputFolder = QtWidgets.QToolButton(parent=self.gridLayoutWidget)
        self.btnSelectInputFolder.setObjectName("btnSelectInputFolder")
        self.gridLayout.addWidget(self.btnSelectInputFolder, 0, 3, 1, 1)
        self.txtOutputFolder = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtOutputFolder.setObjectName("txtOutputFolder")
        self.txtOutputFolder.setReadOnly(True)
        self.txtInputFolder.setReadOnly(True)
        self.gridLayout.addWidget(self.txtOutputFolder, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.btnSelectOutputFolder = QtWidgets.QToolButton(parent=self.gridLayoutWidget)
        self.btnSelectOutputFolder.setObjectName("btnSelectOutputFolder")
        self.gridLayout.addWidget(self.btnSelectOutputFolder, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtInitials = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtInitials.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txtInitials.setObjectName("txtInitials")
        self.gridLayout.addWidget(self.txtInitials, 2, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 600, 158))
        self.tableWidget.setMinimumSize(QtCore.QSize(600, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.btnProcessFiles = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnProcessFiles.setGeometry(QtCore.QRect(630, 270, 100, 23))
        self.btnProcessFiles.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnProcessFiles.setEnabled(False)
        self.btnProcessFiles.setObjectName("btnProcessFiles")
        MicroVuProcessorMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MicroVuProcessorMainWindow)
        self.statusbar.setObjectName("statusbar")
        MicroVuProcessorMainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MicroVuProcessorMainWindow)




    def retranslateUi(self, MicroVuProcessorMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MicroVuProcessorMainWindow.setWindowTitle(_translate("MicroVuProcessorMainWindow", "MicroVu 1Factory Processor"))
        self.btnSelectInputFolder.setText(_translate("MicroVuProcessorMainWindow", "..."))
        self.label.setText(_translate("MicroVuProcessorMainWindow", "Input Folder:  "))
        self.label_2.setText(_translate("MicroVuProcessorMainWindow", "Output Folder:  "))
        self.label_3.setText(_translate("MicroVuProcessorMainWindow", "Initials:  "))
        self.btnSelectOutputFolder.setText(_translate("MicroVuProcessorMainWindow", "..."))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MicroVuProcessorMainWindow", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MicroVuProcessorMainWindow", "MicroVuName"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MicroVuProcessorMainWindow", "IsProfile"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.btnProcessFiles.setText(_translate("MicroVuProcessorMainWindow", "Do It."))
