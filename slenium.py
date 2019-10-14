from  selenium import webdriver as wd
import time as t
from selenium.webdriver.common.keys import Keys


''' Global variables'''
url_g            = "https://www.google.com/"
drive_link_g      = "C:\AT_UD\Auto_update\Drive\chromedriver.exe"
finding_content_g =  "Xi Jing Ping"
target_ele_name_g =  "q"

class gettingInforFromWeb:
    def __init__(self,target_ele_name,url,finding_content):
        self.target_ele_name = target_ele_name
        self.url = url
        self.finding_content = finding_content

    def action(self):
        Finder_Sounder_of_Water = wd.Chrome(drive_link_g)
        Finder_Sounder_of_Water.get(self.url)
        t.sleep(2)
        google = Finder_Sounder_of_Water.find_element_by_name( self.target_ele_name)
        google.send_keys(self.finding_content)
        google.send_keys(Keys.ENTER)


Jonathan = gettingInforFromWeb(target_ele_name_g, url_g, finding_content_g)
Jonathan.action()