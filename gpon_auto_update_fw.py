import time
import os ,sys
import re
from PyQt5.QtCore import *
from selenium import webdriver
from PyQt5 import QtCore, QtGui, QtWidgets
from auto_update.UI_module.AT_UD import *
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
stop_flag = 0
''' -->> global veriables  <<---'''
link_upgrade = 'http://192.168.1.1/cgi-bin/tools_update.asp'
link_login = 'http://192.168.1.1/cgi-bin/login.asp'
link_logged = 'http://192.168.1.1/cgi-bin/index.asp'
link_status = 'http://192.168.1.1/cgi-bin/status_deviceinfo.asp'
link_maintannance = 'http://192.168.1.1/cgi-bin/tools_system.asp'
current_folder = os.getcwd()
firefox_exe_file = current_folder + '\Firefox\Firefox.exe'
print('firefox_exe_file :',firefox_exe_file )
firefox_binary_var = FirefoxBinary(firefox_exe_file)
#driver = webdriver.Firefox(firefox_binary=firefox_binary_var)
#dst_driver = src_driver + "\Drive\chromedriver.exe"
#driver = webdriver.Firefox()


class Main_Process(QThread):
    #alert =pyqtSignal()
    def __init__(self,parent = None):
        QThread.__init__(self, parent)
        self.driver = webdriver.Firefox(firefox_binary=firefox_binary_var)

    def login_ui(self, cur_pw):
        try:
            self.driver.get(link_login)
        except Exception as e:
            print(e)
            return False

        print('self.driver.session_id = ', self.driver.session_id)
        log_times_num = 0
        log_flag = 1
        def_pass = 'AABB012340'
        try:
            while log_flag:
                if self.driver.current_url == link_logged:
                    break
                log_times_num += 1
                if log_times_num < 3:
                    try:
                        self.driver.find_element_by_id("username").send_keys("admin")
                        self.driver.find_element_by_id("password").send_keys(cur_pw)
                        self.driver.find_element_by_id("buttoncolor").click()
                        if self.driver.current_url == link_logged:
                            print('login function return true !')
                            return True
                    except Exception as e:
                        print(e)
                        return False

                else:
                    time.sleep(0.5)
                    try:
                        self.driver.find_element_by_id("username").send_keys("admin")
                        self.driver.find_element_by_id("password").send_keys(def_pass)
                        self.driver.find_element_by_id("buttoncolor").click()
                        if self.driver.current_url == link_logged:
                            print("Logged in with default password after times: ")
                            print('login function return true !')
                            return True
                    except Exception as e:
                        print(e)
                        return False

        except Exception as e:
            print(e)
            return False
        finally:
            print('finally log-in block ')

    def check_connection_ui(self):
        cmd = "ping 192.168.1.1 -n 1"
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
        # time.sleep(1)

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
        ip_buffer = os.popen((ip_cmd)).read()
        buffer = re.findall(r'[\w-]+[\w-]{10}', ip_buffer)
        # mac=None
        if len(buffer) >= 1:
            mac = (''.join(buffer[0])).upper()
            print(mac)
            return mac
        else:
            print('can not get MAC')
            return False

    def getCurrentFw_ui(self):
        try:
            print('self.driver.session_id = ', self.driver.session_id)
            self.driver.get(link_status)
            data = self.driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr[3]/td[3]')
            Current_FW = data.text
            print('Current_FW = ', Current_FW)
            return Current_FW
        except Exception as e:
            print('Can not get current fw !')
            print(e)
            return False

    def up_fw_ui(self, filename):
        try:
            print('self.driver.session_id = ', self.driver.session_id)
            fw_directory = os.getcwd() + '\Firmware\{}'.format(filename)
            print('fw_directory = os.getcwd() + \Firmware\{}.format(filename)')
            print(fw_directory)
            self.driver.get(link_upgrade)
            self.driver.find_element_by_name("tools_FW_UploadFile").send_keys(fw_directory)
            self.driver.find_element_by_name("FW_apply").click()
            while 1:
                try:
                    data = self.driver.find_element_by_tag_name('font')
                    str_success = data.text
                    print('find_element_by_tag_name data = ', str_success)
                    pattern_en = r'File upload succeeded, starting flash erasing and programming!!'
                    pattern_vn = r'Tập tin tải lên thành công, bắt đầu xóa flash và khởi động lại!!'
                    if re.search(pattern_en, str_success) or re.search(pattern_vn, str_success): # or re.search(pattern_en,str_success_ff) or re.search(pattern_vn,str_success_ff):
                        return True
                except Exception as e:
                    print(e)
                    time.sleep(1.5)
                    continue
        except Exception as e:
            print(e)
            return -1

    def check_factory_reset_list_ui(self, MAC):
        with open('factoryRestart.txt') as f:
            if MAC in f.read():
                return 1
            else:
                return 0

    def factory_reset_ui(self):
        try:
            print('self.driver.session_id = ', self.driver.session_id)
            self.driver.get(link_maintannance)
            self.driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr/td[2]/input[3]').click()
            time.sleep(0.2)
            self.driver.switch_to.alert.accept()
            # time.sleep(0.5)
            print('Factory Reset start !')
            return True
        except Exception as e:
            print(e)
            return False

    def get_fw_file_name(self):
        text_data = self.fw_file_name.text()
        buffer = re.findall(r'Ví dụ :', text_data)
        print('get_file_name buffer = ', buffer)
        if buffer:
            return False
        else:
            print('text_data.strip() = ', text_data.strip())
            return text_data.strip()

    def get_fw_target_name_ui(self):
        text_data = self.Fw_target_input.text()
        buffer = re.findall(r'Ví dụ :', text_data)
        print('get_fw_file_name buffer = ', buffer)
        if buffer:
            return False
        else:
            print('text_data.strip() = ', text_data.strip())
            return text_data.strip()

    # def Stop_Program(self):
    #     global stop_flag
    #     stop_flag = 1
    #     print('stop_btn is clicked, stop_flag = ', stop_flag)

    # def creat_thread(self):
    #     main_thread = thr.Thread(target=self.Main_Program)
    #     main_thread.start()
    #
    # def Restart_Program(self):
    #     global stop_flag
    #     stop_flag = 0
    #     print('start_btn is clicked, stop_flag = ', stop_flag)
    #     self.creat_thread()

    def get_pw(self, MAC):
        # MAC = self.getMac_ui()
        if MAC != False:
            mac_split = MAC.split('-')
            pw = str(mac_split[1]) + str(mac_split[2]) + str(mac_split[3]) + str(mac_split[4]) + str(mac_split[5])
            print('pw = ', pw)
            return pw
        else:
            print('Can not get pw')

    def check_correct_fw_ui(self, cur_fw, ui_input_fw):
        if cur_fw == ui_input_fw:
            return True
        else:
            return False

    def Worker_recevier(self):
        self.start()

    def run(self):
        print('Run was called !')
        # ui.display_progress_ui('Program started !!')
        # ui.display_dialog_window_color('background-color: rgb(200, 200, 99);\n', 'color: rgb(36, 36, 36);')
        # ui.display_connection_status_ui('Chờ Kết Nối...')
        print('before while(1)')
        while 1:
            '''-------------check target fw and file name that was manual input-----------------'''
            file_name = self.get_fw_file_name()
            fw_target_name = self.get_fw_target_name_ui()
            if fw_target_name:
                print('fw_target_name (Main_Program) :', fw_target_name)
            else:
                print('please input correctly fw_target_name')
                ui.display_dialog_window_color('background-color: rgb(144, 0, 0);\n', 'color: rgb(255, 255, 255);')
                ui.display_progress_ui('Chưa nhập vào Tên Firware đúng dùng đợt upgrade này(Target FW)\nNhập Tên chính xác và nhấn nút Start để khởi đông lại chuwpng trình')
                time.sleep(6)
                break
            if file_name:
                print('fw_target_name (Main_Program) :', file_name)
            else:
                print('please input correctly fw_target_name')
                ui.display_dialog_window_color('background-color: rgb(144, 0, 0);\n', 'color: rgb(255, 255, 255);')
                ui.display_progress_ui('Chưa nhập vào Tên file firmware\nNhập Tên chính xác và nhấn nút Start để khởi đông lại chương trình')
                time.sleep(6)
                break
            if stop_flag == 1:
                break
            if self.check_connection_ui():
                ui.display_connection_status_ui('Đã kết nối !!')
                #driver = webdriver.Chrome(dst_driver)
                #driver = webdriver.Firefox()
                #driver = webdriver.Firefox(firefox_binary=firefox_binary_var)
                MAC_addr = self.getMac_ui()
                if MAC_addr:
                    print('MAC_addr = ', MAC_addr)
                    current_pw = self.get_pw(MAC_addr)
                    if self.check_Mac_in_list1_ui(MAC_addr):
                        ui.display_update_times('Đã upgrade lần 1')
                    if self.check_Mac_in_list2_ui(MAC_addr):
                        ui.display_update_times('Đã upgrade lần 2')
                    if self.check_factory_reset_list_ui(MAC_addr):
                        ui.display_update_times('Đã Factory reset')
                else:
                    self.driver.close()
                    continue
                if self.login_ui(current_pw):
                    print('inside log_in current_pw = ', current_pw)
                    if self.getCurrentFw_ui():
                        current_fw = self.getCurrentFw_ui()
                        ui.display_Current_FW_ui(current_fw)
                        ui.display_MAC_DUT_ui(MAC_addr)
                    else:
                        print('Can not get Current Fw')
                        self.driver.close()
                        continue
                    if current_fw == fw_target_name and not self.check_Mac_in_list1_ui(MAC_addr) and not self.check_Mac_in_list2_ui(MAC_addr):
                        ui.display_dialog_window_color('background-color: rgb(0, 44, 0);\n','color: rgb(255, 255, 255);')
                        ui.display_progress_ui('Firmware Hiện tại đã là mới nhất,không cần upgrade.\nRút Điện !!!\nChuyển sang bản khác !')
                        self.driver.close()
                        print('self.driver.close()!!!!!!!!!!')
                        continue
                    if self.check_Mac_in_list1_ui(MAC_addr):
                        print('Appeared in List 1,going to check in list 2')
                        ui.display_progress_ui('Đã upgrade lần 1 ,\nĐang tiến hành update lần 2')
                        if self.check_Mac_in_list2_ui(MAC_addr):
                            print('Appeared in List 2  going to check in factory reset list !')
                            ui.display_progress_ui('Đã upgrade lần 2 ,\nKiểm tra Danh sách Factory Reset')
                            if self.check_factory_reset_list_ui(MAC_addr):
                                final_current_fw = self.getCurrentFw_ui()
                                if final_current_fw and (final_current_fw == fw_target_name):
                                    print('Complete !!!')
                                    ui.display_dialog_window_color('background-color: rgb(0, 44, 0);\n','color: rgb(255, 255, 255);')
                                    ui.display_progress_ui('Đã hoàn thành tất các bước !\nRút Điện.\nCắm dầy mạng sang bản khác !!!')
                                    ui.display_connection_status_ui('Chờ Kết nối .....!!')
                                    self.driver.close()
                                    time.sleep(1)
                                    continue
                                else:
                                    # print('Đang kiểm tra bản bản khởi đổng lại thành công chưa')
                                    ui.display_progress_ui(
                                        'Đang kiểm tra bản bản khởi động lại thành công chưa')
                                    self.driver.close()
                                    continue
                            else:
                                print('Start Factory reset')
                                if self.factory_reset_ui():
                                    self.write_Mac_to_factory_reset_ui(MAC_addr)
                                    ui.display_progress_ui(
                                        'KHÔNG ĐƯỢC RÚT ĐIỆN !\nĐang Factory Set !.\nBản Đang khởi động lại \nCó thể cắm dây mạng sang bản khác')
                                    ui.display_update_times('2/2 Đang factory reset')
                                else:
                                    self.driver.close()
                                    continue
                                ui.display_connection_status_ui('Chờ Kết nối..... !!')
                                self.driver.close()
                                time.sleep(8)
                                continue
                        else:
                            if self.getCurrentFw_ui():
                                current_fw_2nd = self.getCurrentFw_ui()
                                print('current_fw_2nd :', current_fw_2nd)
                                ui.display_Current_FW_ui(current_fw)
                            else:
                                print('Can not get current_fw_2nd')
                                self.driver.close()
                                continue
                            if not self.check_correct_fw_ui(current_fw_2nd,fw_target_name) and self.check_Mac_in_list1_ui(MAC_addr) == 1:
                                print('Firm ware not same')
                                ui.display_dialog_window_color('background-color: rgb(165, 0, 0);\n','color: rgb(255, 255, 255);')
                                ui.display_progress_ui('Phiền Bản FW này không đúng!!\nLIÊN HỆ KỸ SƯ XỦ LÝ !!\nChương trình tạm dừng\nBấm nút "Start" để khơi động lại')
                                self.driver.close()
                                break
                            update_status_2 = self.up_fw_ui(file_name)
                            if update_status_2 == True:
                                ui.display_progress_ui("Upgrade lần 2 thành công !!")
                                self.write_Mac_to_list2_ui(MAC_addr)
                                ui.display_progress_ui(
                                    'Tập tin tải lên thành công,\nbắt đầu xóa flash và khởi động lại!!\nĐã upgrade lần 1!.\nĐang tiến hành Upgrade lần 2\nBản Đang khởi động lại \nCó thể cắm dây mạng sang bản khác')
                                ui.display_update_times('Lần 2/2 (file list2.txt) \nCần upgrade 2 lần')
                            elif update_status_2 == -1:
                                ui.display_dialog_window_color('background-color: rgb(165, 0, 0);\n',
                                                                 'color: rgb(255, 255, 255);')
                                ui.display_progress_ui(
                                    'Tên File FW nhập vào không đúng\nVới FW trong thư mực "\Firmware"')
                                self.driver.close()
                                print('InvalidArgumentException in 2nd upgrade')
                                break
                            else:
                                ui.display_progress_ui('Load firmware thất bại !')
                                self.driver.close()
                                continue
                            ui.display_connection_status_ui('Chờ Kết nối.....!!')
                            self.driver.close()
                            time.sleep(15)
                            continue
                    else:
                        self.display_progress_ui('Bản này chưa update lần nào')
                        print('Update lan 1!')
                        update_status_1 = self.up_fw_ui(file_name)
                        if update_status_1 == True:
                            self.display_progress_ui('Upgrade lần 1 thành công !!')
                            self.write_Mac_to_list1_ui(MAC_addr)
                            self.display_progress_ui(
                                'Tập tin tải lên thành công,\nbắt đầu xóa flash và khởi động lại!!\nĐã Upgrade lan 1! \nBản đang khỏi động lại\nCó thể chuyến sang bản khác')
                            self.display_update_times('Lần 1/2 (file list1.txt)\nCần upgrade 2 lần')
                        elif update_status_1 == -1:
                            self.display_dialog_window_color('background-color: rgb(165, 0, 0);\n',
                                                             'color: rgb(255, 255, 255);')
                            self.display_progress_ui(
                                'Tên File FW nhập vào không đúng với FW trong thư mực "\Firmware",\nGiải Pháp : Kiểm Tra lại tên file Fw,ấn nút start để khởi động lại chương trình')
                            self.driver.close()
                            print('InvalidArgumentException in 1st upgrade')
                            break
                        else:
                            self.display_progress_ui('Tải firware thất bại !')
                            self.driver.close()
                            continue
                        ui.display_connection_status_ui('Chờ Kết nối ..... !!')
                        self.driver.close()
                        time.sleep(15)
                        continue
                else:
                    print('waiting for log in')
                    # self.display_progress_ui('Đăng nhập thất bại.\nĐang thử lại')
                    self.driver.close()
                    # time.sleep(0.5)
                    continue
            else:
                # self.display_progress_ui('Checking connection....')
                ui.display_connection_status_ui('Chờ kết nối ...')

class Inheritance_Ui_MainWindow(Ui_MainWindow):
    first_thread = Main_Process()
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        MainWindow.show()
        self.start_btn.clicked.connect(self.Connect_Worker)
        sys.exit(app.exec_())


    # def creat_thread(self):
    #     first_thread = Main_Process()
    #     return  first_thread

    def Connect_Worker(self):
        print('start_btn is clicked')
        self.creat_thread().Worker_recevier()

    def display_start_warning(self):
        self.display_dialog_window_color('background-color: rgb(200, 200, 99);\n', 'color: rgb(36, 36, 36);')
        self.display_progress_ui(
            'Chú Ý Quan Trọng: \n+)File Firmware có dạng "file_name.bin" lưu trong thư mục :"\Firmware".\n'
            '+)Nhập đúng tên file này và tên bản fw sẽ Upgrade vào 2 mục tương ứng là :"Tên File"(chữ màu xanh dương ) và "Tên bản FW upgrade"(chữ màu vàng).\n+)Nhấn nút "Start" để bắt đầu chạy chương trình Upgrade!')

    def display_MAC_DUT_ui(self, input_value):
        self.MAC_DUT.clear()
        self.MAC_DUT.addItem(input_value)

    def display_Current_FW_ui(self, input_fw):
        self.Cur_FW.clear()
        self.Cur_FW.addItem(input_fw)

    def display_progress_ui(self, input_notification):
        self.dialog_window.clear()
        self.dialog_window.addItem(input_notification)

    def display_connection_status_ui(self, input_status):
        self.connection_status.clear()
        self.connection_status.addItem(input_status)
        # self.connection_status.colorCount('')

    def display_update_times(self, input_upgrade_time):
        self.update_times.clear()
        self.update_times.addItem(input_upgrade_time)

    def display_dialog_window_color(self, str_font_color, background_color_str):
        color_str_bg = "{}{}".format(str_font_color, background_color_str)
        self.dialog_window.setStyleSheet(color_str_bg)  # "background-color: rgb(166, 249, 249);"

    def restart_notification(self):
        self.dialog_window.clear()
        self.dialog_window.addItem('Chương trình đang khỏi động lại')



if __name__ == "__main__":
    #app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = Inheritance_Ui_MainWindow()
    #ui.first_thread
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    #sys.exit(app.exec_())

