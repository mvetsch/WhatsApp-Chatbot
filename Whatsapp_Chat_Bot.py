#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
import math
import pickle
from pyvirtualdisplay import Display

local_storage_persistent_file = 'config'
local_storage_keys = {'AR2vvQGmFz8O+X3Q==','Dexie.DatabaseNames', 'ECuqK2dZvWBQr2MauWAKQA==','S++2iNqlOR0a1ri1maFSuA==','WABrowserId', 'WASecretBundle', 'WAToken1', 'WAToken2', 'bQavMP78JENNWiIu7ug/oA==', 'debugCursor', 'fhM1SFL98ULqVx5VadTyxA==', 'last-wid', 'logout-token', 'remember-me', 'storage_test', 'whatsapp-mutex'}

display = Display(visible=0, size=(1920, 1080))
display.start()

class Message():
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __eq__(self, other):
        return self.message == other.message


def store_local_storage(driver):
    driver.switch_to_window(driver.window_handles[0])
    data = {}
    for key in local_storage_keys:
        data[key] = driver.execute_script("return window.localStorage.getItem('" + key + "');")

    pickle.dump(data, open('config', 'w'))

def restore_local_storage(driver):
    driver.switch_to_window(driver.window_handles[0])
    data = pickle.load(open('config', 'r'))
    for key in data:
        driver.execute_script("window.localStorage.setItem('" + key + "','" + str(data[key]) + "');");


driverPath = "driver/chromedriver"
dataPath = "Data/ChatBot"

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + dataPath)
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://web.whatsapp.com')
if os.path.exists('config'):
    print 'restore localStorage' 
    restore_local_storage(driver)
driver.get('https://web.whatsapp.com')
driver.switch_to_window(driver.window_handles[0])

chatHistory = []
replyQueue = []
firstRun = True

print("Starting...")

def view_is_loaded():
    try:
        driver.find_element_by_id("pane-side")
        return True
    except:
        return False 

while not view_is_loaded():  
    print 'sleep some time until it is loaded' 
    time.sleep(1)

target = sys.argv[1]
message = sys.argv[2]

open_chats = driver.find_elements_by_class_name("chat-title")

for l in open_chats:
    if l.text.startswith(target):
        l.click()



right = driver.find_element_by_id("main")
inputf = right.find_element_by_class_name("pluggable-input-body");
inputf.click()
print dir(inputf)
inputf.send_keys(message)

button = right.find_element_by_class_name("compose-btn-send");
button.click()

store_local_storage(driver)
