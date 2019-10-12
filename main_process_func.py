from PyQt5 import QtCore,QtGui,QtWidgets
from Qt.auto_update.AT_UD import *
from functools import wraps



@Qt.auto_update.AT_UD.setupUI
def hahaha(self):
    print(self)


class Inheritance_Ui_MainWindow(Ui_MainWindow):
    def Manual_input_FW(self):
        value = self.Fw_name_input.text()
        self.Fw_name_input.clear()
        self.MAC_DUT.clear()
        self.MAC_DUT.addItem(value)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Inheritance_Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



