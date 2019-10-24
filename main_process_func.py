from PyQt5 import QtCore,QtGui,QtWidgets
import threading as thr
import sys
from  selenium import webdriver
from  selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import expected_conditions
from  selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time
import os
import re
from auto_update import AT_UD
stop_flag = 0
''' -->> global veriables  <<---'''
link_upgrade        = 'http://192.168.1.1/cgi-bin/tools_update.asp'
link_login          = 'http://192.168.1.1/cgi-bin/login.asp'
link_logged         = 'http://192.168.1.1/cgi-bin/index.asp'
link_status         = 'http://192.168.1.1/cgi-bin/status_deviceinfo.asp'
link_maintannance   = 'http://192.168.1.1/cgi-bin/tools_system.asp'
src_driver = os.getcwd()
dst_driver = src_driver + "\Drive\chromedriver.exe"
driver = webdriver.Chrome(dst_driver)

class Inheritance_Ui_MainWindow(AT_UD.Ui_MainWindow):

    def login_ui(self):
        def handle_alert():
            driver.switch_to.alert.accept()
        driver.get(link_login)
        print('driver.session_id = ', driver.session_id)
        log_times_num = 0
        log_flag = 1
        cur_pw = self.get_pw()
        def_pass = 'AABB012340'
        try:
            while log_flag:
                # if driver.current_url == link_logged:
                #     break
                log_times_num += 1
                if log_times_num < 3:
                    try:
                        driver.find_element_by_id("username").send_keys("admin")
                        driver.find_element_by_id("password").send_keys(cur_pw)
                        driver.find_element_by_id("buttoncolor").click()
                        if driver.current_url == link_logged:
                            print('login function return true !')
                            return True
                    except :
                        #driver.close()
                        self.Restart_Program()
                else:
                    time.sleep(0.5)
                    try:
                        driver.find_element_by_id("username").send_keys("admin")
                        driver.find_element_by_id("password").send_keys(def_pass)
                        driver.find_element_by_id("buttoncolor").click()
                        if driver.current_url == link_logged:
                            print("Logged in with default password after times: ")
                            print('login function return true !')
                            return True
                    except:
                        #driver.close()
                        self.Restart_Program()
        except UnexpectedAlertPresentException :
            print('UnexpectedAlertPresentException')
            handle_alert()
            #driver.close()
            self.Restart_Program()
            return False
        except NoAlertPresentException :
            #print('if Login func rasing an exception, comback start program loop !!!')
            #driver.close()
            self.Restart_Program()
            return False
        finally:
            #driver.close()
            self.Restart_Program()
    def check_connection_ui(self):
        cmd = "ping 192.168.1.1 -n 3"
        pattern = r'Lost = 0'
        while 1:
            cmd_buffer = os.popen(cmd).read()
            flag = re.search(pattern, cmd_buffer)
            if flag:
                print('Connected!')
                return 1
            else:
                print("Not Connect!")
                return 0
        #time.sleep(1)


    def write_Mac_to_list1_ui(self, MAC):
        text_file = open("list1.txt", "a")
        text_file.write("%s\n" % (MAC))
        text_file.close()

    def write_Mac_to_list2_ui(self, MAC):
        text_file = open("list2.txt", "a")
        text_file.write("%s\n" % (MAC))
        text_file.close()

    def write_Mac_to_factory_reset_ui(self, MAC):
        text_file = open("factoryRestart.txt", "a")
        text_file.write("%s\n" % (MAC))
        text_file.close()

    def check_Mac_in_list1_ui(self, MAC):
        with open('list1.txt') as f:
            if MAC in f.read():
                return 1
            else:
                return 0

    def check_Mac_in_list2_ui(self, MAC):
        with open('list2.txt') as f:
            if MAC in f.read():
                return 1
            else:
                return 0

    def getMac_ui(self):
        ip_cmd = 'arp -a 192.168.1.1'
        while 1:
            ip_buffer = os.popen((ip_cmd)).read()
            buffer = re.findall(r'[\w-]+[\w-]{10}', ip_buffer)
            if len(buffer) >= 1:
                mac = (''.join(buffer[0])).upper()
                break
            else:
                print('can not get MAC')
            time.sleep(1)
        print(mac)
        return mac

    def getCurrentFw_ui(self):
        try:
            print('driver.session_id = ', driver.session_id)
            driver.get(link_status)
            data = driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr[3]/td[3]')
            Current_FW = data.text
            print('Current_FW = ', Current_FW)
            return Current_FW
        except:
            print('Can not get current fw !')
            self.Restart_Program()

    def up_fw_ui(self,filename):
        try:
            print('driver.session_id = ', driver.session_id)
            fw_directory = os.getcwd() + '\Firmware\/{}'.format(filename)
            driver.get(link_upgrade)
            driver.find_element_by_name("tools_FW_UploadFile").send_keys(fw_directory)
            driver.find_element_by_name("FW_apply").click()
            while 1:
                time.sleep(0.5)
                data = driver.find_element_by_tag_name('font')
                str_success = data.text
                print('data = ', str_success)
                pattern_en = r'File upload succeeded, starting flash erasing and programming!!'
                pattern_vn = r'Tập tin tải lên thành công, bắt đầu xóa flash và khởi động lại!!'
                if re.search(pattern_en, str_success) or re.search(pattern_vn, str_success):
                    return True
                else:
                    return False
        except:
            self.Restart_Program()

    def check_factory_reset_list_ui(self,MAC):
        with open('factoryRestart.txt') as f:
            if MAC in f.read():
                return 1
            else:
                return 0

    def factory_reset_ui(self):
        try:
            print('driver.session_id = ', driver.session_id)
            driver.get(link_maintannance)
            driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr/td[2]/input[3]').click()
            time.sleep(0.2)
            driver.switch_to.alert.accept()
            time.sleep(0.5)
        except:
            self.Restart_Program()

    def display_MAC_DUT_ui(self,input_value):
        self.MAC_DUT.clear()
        self.MAC_DUT.addItem(input_value)

    def display_Current_FW_ui(self,input_fw):
        self.Cur_FW.clear()
        self.Cur_FW.addItem(input_fw)

    def display_progress_ui(self,input_notification):
        self.dialog_window.clear()
        self.dialog_window.addItem(input_notification)

    def display_connection_status_ui(self,input_status):
        self.connection_status.clear()
        self.connection_status.addItem(input_status)
     #   self.connection_status.colorCount('')

    def display_update_times(self,input_upgrade_time):
        self.update_times.clear()
        self.update_times.addItem(input_upgrade_time)

    def restart_notification(self):
        self.dialog_window.clear()
        self.dialog_window.addItem('Chương trình đang khỏi động lại')

    def get_fw_file_name(self):
        return self.fw_file_name.text()

    def get_fw_input_name_ui(self):
        return self.Fw_name_input.text()

    def Stop_Program(self):
        global stop_flag
        stop_flag = 1
        print('stop_btn is clicked, stop_flag = ', stop_flag)

    def creat_thread(self):
        main_thread = thr.Thread(target=self.Main_Program)
        main_thread.start()

    def Restart_Program(self):
        global stop_flag
        stop_flag = 0
        print('start_btn is clicked, stop_flag = ', stop_flag)
        self.creat_thread()

    def get_pw(self):
        MAC = self.getMac_ui()
        mac_split = MAC.split('-')
        pw = str(mac_split[1]) + str(mac_split[2]) + str(mac_split[3]) + str(mac_split[4]) + str(mac_split[5])
        print('pw = ', pw)
        return pw

    def check_correct_fw_ui(self,cur_fw, ui_input_fw):
        if cur_fw == ui_input_fw:
            return True
        else:
            return False
    def Main_Program(self):
        driver = webdriver.Chrome(dst_driver)
        self.display_progress_ui('Program started !!')
        self.display_connection_status_ui('Chờ Kết Nối...')
        file_name = self.get_fw_file_name()
        fw_input_name = self.get_fw_input_name_ui()
        print('fw_input_name :', fw_input_name)
        while 1:
            if stop_flag == 1:
                break
            if self.check_connection_ui():
                self.display_connection_status_ui('Đã kết nối !!')
                #driver = webdriver.Chrome(dst_driver)
                if self.login_ui():
                    MAC_addr = self.getMac_ui()
                    current_fw = self.getCurrentFw_ui()
                    self.display_Current_FW_ui(current_fw)
                    self.display_MAC_DUT_ui(MAC_addr)
                    if current_fw == fw_input_name and not self.check_Mac_in_list1_ui(MAC_addr):
                        self.display_progress_ui('Firmware đã OK.\nRút Điện !!!\nChuyển sang bản khác !')
                        driver.close()
                        continue
                    if self.check_Mac_in_list1_ui(MAC_addr):
                        print('Appeared in List 1,going to check in list 2')
                        self.display_progress_ui('Đã upgrade lần 1 ,\nĐang tiến hành update lần 2')
                        if self.check_Mac_in_list2_ui(MAC_addr):
                            print('Appeared in List 2  going to check in factory reset list !')
                            self.display_progress_ui('Đã upgrade lần 2 ,\nKiểm tra Danh sách Factory Reset')
                            if self.check_factory_reset_list_ui(MAC_addr):
                                print('Complete !!!')
                                self.display_progress_ui(
                                    'Đã hoàn thành tất các bước !\nRút Điện.\nCắm dầy mạng sang bản khác !!!')
                                self.display_connection_status_ui('Chờ Kết nối .....!!')
                                driver.close()
                                continue
                            else:
                                print('Start Factory reset')
                                self.factory_reset_ui()
                                self.write_Mac_to_factory_reset_ui(MAC_addr)
                                self.display_progress_ui(
                                    'KHÔNG ĐƯỢC RÚT ĐIỆN !\nĐang Factory Set !.\nBản Đang khởi động lại \nCó thể cắm dây mạng sang bản khác')
                                self.display_update_times('Đã update 2/2 lần \nĐang Factory Reset')
                                self.display_connection_status_ui('Chờ Kết nối..... !!')
                                driver.close()
                                time.sleep(8)
                                continue
                        else:
                            current_fw_2nd = self.getCurrentFw_ui()
                            print('current_fw_2nd :', current_fw_2nd)
                            self.display_Current_FW_ui(current_fw)
                            if  not self.check_correct_fw_ui(current_fw_2nd, fw_input_name) and not self.check_Mac_in_list1_ui(MAC_addr):
                                print('Firm ware not same')
                                self.display_progress_ui('Phiền Bản FW này không đúng!!\nLIÊN HỆ KỸ SƯ XỦ LÝ !!\nChương trình tạm dừng\nBấm nút "Start" để khơi động lại')
                                break
                            if self.up_fw_ui(file_name):
                                self.display_progress_ui("Upgrade lần 2 thành công !!")
                                #driver.close()
                            else:
                                self.display_progress_ui('load firware thất bại !')
                                #driver.close()

                            self.write_Mac_to_list2_ui(MAC_addr)
                            self.display_progress_ui('Tập tin tải lên thành công,\nbắt đầu xóa flash và khởi động lại!!\nĐã upgrade lần 1!.\nĐang tiến hành Upgrade lần 2\nBản Đang khởi động lại \nCó thể cắm dây mạng sang bản khác')
                            self.display_update_times('Lần 2/2 (file list2.txt) \nCần upgrade 2 lần')
                            self.display_connection_status_ui('Chờ Kết nối.....!!')
                            driver.close()
                            time.sleep(18)
                            continue
                    else:
                        self.display_progress_ui('Chưa update lần nào')
                        print('Update lan 1!')
                        if self.up_fw_ui(file_name):
                            self.display_progress_ui('Upgrade lần 1 thành công !!')
                        else:
                            self.display_progress_ui('Tải firware thất bại !')
                            continue
                        self.write_Mac_to_list1_ui(MAC_addr)
                        self.display_progress_ui(
                            'Tập tin tải lên thành công,\nbắt đầu xóa flash và khởi động lại!!\nĐã Upgrade lan 1! \nBản đang khỏi động lại\nCó thể chuyến sang bản khác')
                        self.display_update_times('Lần 1/2 (file list1.txt)\nCần upgrade 2 lần')
                        self.display_connection_status_ui('Chờ Kết nối ..... !!')
                        driver.close()
                        time.sleep(18)
                        continue
                else:
                    print('waiting for log in')
                    self.display_progress_ui('Chờ đăng nhập')
            else:
                self.display_progress_ui('Checking connection....')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Inheritance_Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    ui.restart_btn.clicked.connect(ui.Restart_Program)
    ui.stop_btn.clicked.connect(ui.Stop_Program)
    sys.exit(app.exec_())



