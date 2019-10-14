from PyQt5 import QtCore,QtGui,QtWidgets
from Auto_update.AT_UD import Ui_MainWindow


class Inheritance_Ui_MainWindow(Ui_MainWindow):
    def Manual_input_FW(self):
        value = self.Fw_name_input.text()
        self.Fw_name_input.clear()
        self.MAC_DUT.clear()
        self.MAC_DUT.addItem(value)
    def Run_click(self,w):
        self.FW_btn_confirm.clicked.connect(self.Manual_input_FW)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Inheritance_Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.Run_click(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



