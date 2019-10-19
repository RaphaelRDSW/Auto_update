from PyQt5 import QtCore,QtGui,QtWidgets
import threading as thr
import sys
from  selenium import webdriver as wd
import time
from selenium.webdriver.common.keys import Keys
import os
import re

from auto_update import selenium_func
from auto_update import AT_UD

class Inheritance_Ui_MainWindow(AT_UD.Ui_MainWindow):
    def login_ui(self):
        selenium_func.login()

    def check_connection_ui(self):
        return selenium_func.check_connection()

    def write_Mac_to_list1_ui(self, MAC):
        return selenium_func.write_Mac_to_list1(MAC)

    def write_Mac_to_list2_ui(self, MAC):
        return selenium_func.write_Mac_to_list2(MAC)

    def write_Mac_to_factory_reset_ui(self, MAC):
        return selenium_func.write_Mac_to_Factory_Reset_List(MAC)

    def check_Mac_in_list1_ui(self, MAC):
        return selenium_func.check_Mac_in_list1(MAC)

    def check_Mac_in_list2_ui(self, MAC):
        return selenium_func.check_Mac_in_list2(MAC)

    def getMac_ui(self):
        return selenium_func.get_MAC()

    def getCurrentFw_ui(self):
        selenium_func.get_curent_fw()
        return selenium_func.Current_FW

    def up_fw_ui(self):
        return selenium_func.up_fw()

    def check_factory_reset_list_ui(self,MAC):
        return selenium_func.check_Mac_in_Factoy_Reset_List(MAC)

    def factory_reset_ui(self):
        return selenium_func.factory_reset()

    def display_MAC_DUT_ui(self,input_value):
        self.MAC_DUT.clear()
        self.MAC_DUT.addItem(input_value)

    def display_Current_FW_ui(self,input_fw):
        self.Cur_FW.clear()
        self.Cur_FW.addItem(input_fw)

    def display_progress_ui(self,input_notification):
        self.dialog_window.clear()
        self.dialog_window.addItem(input_notification)



def Start_Program():
    while 1:
        if ui.check_connection_ui():
            selenium_func.driver = wd.Chrome(selenium_func.dst_driver)
            ui.login_ui()
            MAC_addr = ui.getMac_ui()
            current_fw = ui.getCurrentFw_ui()
            ui.display_Current_FW_ui(current_fw)
            ui.display_MAC_DUT_ui(MAC_addr)
            if ui.check_Mac_in_list1_ui(MAC_addr):
                print('Appeared in List 1,going to check in list 2')
                ui.display_progress_ui('Đã upgrade lần 1 , Đang tiến hành update lần 2')
                if ui.check_Mac_in_list2_ui(MAC_addr):
                    print('Appeared in List 2  going to check in factory reset list !')
                    ui.display_progress_ui('Đã upgrade lần 2 , Kiểm tra Danh sách Factory Reset')
                    if ui.check_factory_reset_list_ui(MAC_addr):
                        print('Complete !!!')
                        ui.display_progress_ui('Đã hoàn thành tất các bước !\nRút Điện.\nChuyển sang bản khác !!!')
                        selenium_func.driver.close()
                        continue
                    else:
                        print('Start Factory reset')
                        ui.factory_reset_ui()
                        ui.write_Mac_to_factory_reset_ui(MAC_addr)
                        ui.display_progress_ui('KHÔNG ĐƯỢC RÚT ĐIỆN !\nĐang Factory Set !.\nBản Đang khởi động lại \nCó thể chuyển sang bản khác')
                        selenium_func.driver.close()
                        time.sleep(15)
                        continue
                else:
                    ui.up_fw_ui()
                    ui.write_Mac_to_list2_ui(MAC_addr)
                    ui.display_progress_ui('Đã upgrade lần 1!.\nĐang tiến hành Upgrade lần 2\nBản Đang khởi động lại \nCó thể chuyển sang bản khác')
                    time.sleep(15)
                    continue
            else:
                ui.display_progress_ui('chưa update lần nào')
                print('Update lan 1!')
                ui.up_fw_ui()
                ui.write_Mac_to_list1_ui(MAC_addr)
                ui.display_progress_ui('Đã Upgrade lan 1! \nBản đang khỏi động lại\nCó thể chuyến sang bản khác')
                time.sleep(15)
                continue
        time.sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Inheritance_Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    '''------- Creat main thread independ with ui thread-------------'''
    main_thread = thr.Thread(target=Start_Program)
    main_thread.start()

    sys.exit(app.exec_())



