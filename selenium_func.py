from  selenium import webdriver as wd
import time
from selenium.webdriver.common.keys import Keys
import os
import re
#from auto_update import main_process_func
''' -->> global veriables  <<---'''
link_upgrade        = 'http://192.168.1.1/cgi-bin/tools_update.asp'
link_login          = 'http://192.168.1.1/cgi-bin/login.asp'
link_logged         = 'http://192.168.1.1/cgi-bin/index.asp'
link_status         = 'http://192.168.1.1/cgi-bin/status_deviceinfo.asp'
link_maintannance   = 'http://192.168.1.1/cgi-bin/tools_system.asp'
src_driver = os.getcwd()
dst_driver = src_driver + "\Drive\chromedriver.exe"
#Current_FW = ''
mac = ''
driver = wd.Chrome(dst_driver)
#driver = None

def check_connection():
    cmd         = "ping 192.168.1.1 -n 1"
    pattern     = r'Lost = 0'
    cmd_buffer  = os.popen(cmd).read()
    flag = re.search(pattern, cmd_buffer)
    if flag:
        print('Connected!')
        return 1
    else:
        print("Not Connect!")
        return 0

def login():
    print('driver.session_id = ',driver.session_id)
    log_times_num = 0
    log_flag = 1
    cur_pw = get_pw()
    def_pass = 'AABB012340'
    driver.get(link_login)
    try:
        while log_flag:
            if driver.current_url == link_logged:
                break
            log_times_num += 1
            if log_times_num < 3:
                driver.find_element_by_id("username").send_keys("admin")
                driver.find_element_by_id("password").send_keys(cur_pw)
                driver.find_element_by_id("buttoncolor").click()
                if driver.current_url == link_logged:
                    print('driver.current_url = ',driver.current_url)
                    break
            else:
                time.sleep(0.5)
                driver.find_element_by_id("username").send_keys("admin")
                driver.find_element_by_id("password").send_keys(def_pass)
                driver.find_element_by_id("buttoncolor").click()
                if driver.current_url == link_logged:
                    print ("Logged in with default password after times: ")
                    break
    except:
        print('if Login func rasing an exception, comback start program loop !!!')
        Restart_Program()


def up_fw(filename):
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
            print('data = ',str_success)
            pattern_en = r'File upload succeeded, starting flash erasing and programming!!'
            pattern_vn = r'Tập tin tải lên thành công, bắt đầu xóa flash và khởi động lại!!'
            if re.search(pattern_en,str_success) or re.search(pattern_vn,str_success):
                return True
            else:
                return False
    except:
        Restart_Program()

def get_MAC():
    ip_cmd      = 'arp -a 192.168.1.1'
    while 1:
        ip_buffer = os.popen(ip_cmd).read()
        buffer = re.findall(r'[\w-]+[\w-]{10}', ip_buffer)
        if len(buffer) >= 1:
            global mac
            mac = (''.join(buffer[0])).upper()
            break
        else:
            print('can not get MAC')
        time.sleep(1)
    print(mac)
    return mac

def get_pw():
    MAC = get_MAC()
    mac_split = MAC.split('-')
    pw = str(mac_split[1]) + str(mac_split[2]) + str(mac_split[3]) + str(mac_split[4]) + str(mac_split[5])
    print('pw = ',pw)
    return pw

def write_Mac_to_list1(mac):
    text_file = open("list1.txt", "a")
    text_file.write("%s\n" %(mac))
    text_file.close()

def write_Mac_to_list2(mac):
    text_file = open("list2.txt", "a")
    text_file.write("%s\n" %(mac))
    text_file.close()

def write_Mac_to_Factory_Reset_List(mac):
    text_file = open("factoryRestart.txt", "a")
    text_file.write("%s\n" %(mac))
    text_file.close()

def check_Mac_in_list1(mac):
    with open('list1.txt') as f :
        if mac in f.read():
            return 1
        else:
            return 0

def check_Mac_in_list2(mac):
    with open('list2.txt') as f :
        if mac in f.read():
            return 1
        else:
            return 0

def check_Mac_in_Factoy_Reset_List(MAC):
    with open('factoryRestart.txt') as f :
        if MAC in f.read():
            return 1
        else:
            return 0

def get_curent_fw():
    try:
        print('driver.session_id = ', driver.session_id)
        driver.get(link_status)
        data = driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr[3]/td[3]')
        Current_FW = data.text
        print('Current_FW = ', Current_FW)
        return Current_FW
    except:
        Restart_Program()

def factory_reset():
    try:
        print('driver.session_id = ', driver.session_id)
        driver.get(link_maintannance)
        driver.find_element_by_xpath('//*[@id="block1"]/table[2]/tbody/tr/td[2]/input[3]').click()
        time.sleep(0.2)
        driver.switch_to.alert.accept()
        time.sleep(0.5)
    except:
        Restart_Program()

def check_correct_fw(cur_fw, ui_input_fw):
    if cur_fw == ui_input_fw:
        return True
    else:
        return False


if __name__ == '__main__':
    print(check_correct_fw('aaa',"aaa"))
    login()
    print('waiting for connect ! Pinging ')
