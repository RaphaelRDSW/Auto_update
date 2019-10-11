# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\AT_UD\Auto_update\AT_UD.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(434, 583)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setObjectName("label")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 40, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 120, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(320, 450, 91, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 210, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 370, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setObjectName("label_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(170, 160, 241, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.MAC_DUT = QtWidgets.QListWidget(self.centralwidget)
        self.MAC_DUT.setGeometry(QtCore.QRect(170, 40, 256, 31))
        self.MAC_DUT.setObjectName("MAC_DUT")
        self.Cur_FW = QtWidgets.QTreeView(self.centralwidget)
        self.Cur_FW.setGeometry(QtCore.QRect(170, 80, 256, 31))
        self.Cur_FW.setObjectName("Cur_FW")
        self.Updating_FW = QtWidgets.QTreeView(self.centralwidget)
        self.Updating_FW.setGeometry(QtCore.QRect(170, 120, 256, 31))
        self.Updating_FW.setObjectName("Updating_FW")
        self.Updating_FW_2 = QtWidgets.QTreeView(self.centralwidget)
        self.Updating_FW_2.setGeometry(QtCore.QRect(10, 250, 411, 91))
        self.Updating_FW_2.setObjectName("Updating_FW_2")
        self.Updating_FW_3 = QtWidgets.QTreeView(self.centralwidget)
        self.Updating_FW_3.setGeometry(QtCore.QRect(10, 410, 171, 121))
        self.Updating_FW_3.setObjectName("Updating_FW_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 434, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.start_btn.clicked.connect(self.addtem_func)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Auto-Update-Firware"))
        self.label_1.setText(_translate("MainWindow", "MAC của DUT"))
        self.label_2.setText(_translate("MainWindow", "FW Hiện Tại"))
        self.label_5.setText(_translate("MainWindow", "FW Sẽ Update "))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.label_3.setText(_translate("MainWindow", "Thông Báo"))
        self.label_4.setText(_translate("MainWindow", "Kết Quả"))
        self.label_6.setText(_translate("MainWindow", "Tải FW vào DUT"))

    def addtem_func(self):
        value = 'AAAAAAAAA'
        self.MAC_DUT.addItem(value) # Add the value we got to the list


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
