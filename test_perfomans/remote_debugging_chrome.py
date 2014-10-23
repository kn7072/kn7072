# -*- coding:utf-8 -*-
from selenium import webdriver

import unittest
import websocket
import socket
from http.client import HTTPConnection, HTTPSConnection, OK

# options = webdriver.ChromeOptions()
# #options.add_argument(r"--user-data-dir=C:\Users\sv.dokuchaev\AppData\Local\Google\Chrome\User Data")
# options.add_argument("-incognito")
import requests


#super().setUpClass()
#cls.run_chrome(cls)
options = webdriver.ChromeOptions()
#options.add_argument(r"--remote-debugging-port=9222")  # 9222
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# #options.add_argument('--allow-running-insecure-content')
#options.add_argument("--user-data-dir=D:/prof2/chrome2/xxx")
options.add_argument(r'--remote-shell-port=33333')
options.add_argument(r'--log-path=C:\somelogfile.log')
options.add_argument(r'--verbose')
#options.add_experimental_option("debuggerAddress", "localhost:92222")
# options.add_argument(r"--user-data-dir=kllll")  # remoute77777  D:\chome_prof
#options.add_argument(r'--remote-debugging-port=9222') #--debuggerAddress=localhost:55555  http://localhost:28900/json
#options.add_argument(r'--window-size=400,400')
#options.add_argument("-incognito")
#driver = webdriver.Chrome(chrome_options=options)  #, port=55555 chrome_options=options

CHROME_ = {
    "browserName": "chrome",
    "version": "",
    "platform": "ANY",
    'chrome.switches':['remote-debugging-port=9222']
    }
CHROME_['chromeOptions'] = {}
CHROME_['chromeOptions']['args'] = ['--window-size=700,700', '--port=77777']  #, '--remote-debugging-port=9222','--remote-shell-port=9222 ' , 'debuggerAddress=localhost:77777'

#"chrome.switches": ['window-size=300,400']
#chrome.switches# 'debuggerAddress=localhost:77755'
#"remote-debugging-port=9222"

caps = webdriver.DesiredCapabilities.CHROME
caps['chromeOptions'] = {}
caps['chromeOptions']['args'] = ['window-size=400,400', 'window-position=200,300','user-data-dir=D:/prof2/chrome2/xxx', 'remote-shell-port=33333']  #,'remote-debugging-port=9222' , 'user-data-dir=C:/Users/sg.chernov/AppData/Local/Google/Chrome/User Data/Default_1'

#, 'debuggerAddress=127.0.0.1:77777'--remote-debugging-port=9222

# user-data-dir=C:\Users\sg.chernov\AppData\Local\Google\Chrome\User Data
#cls.driver = webdriver.Chrome(desired_capabilities=CHROME_)
# "C:\Documents and Settings\bob\Local Settings\Application Data\Google\Chrome\Application\chrome.exe" --user-data-dir="S:\Profiles\bob"

# "chromeOptions":{"args":['window-size=800,300', 'window-position=200,300', 'user-data-dir=D:/prof2/chrome2/xxx']}
driver = webdriver.Remote(command_executor='http://192.168.1.2:4444/wd/hub', desired_capabilities=caps)  #grid/register  , desired_capabilities=caps
print()
driver = webdriver.Chrome(chrome_options=options)  #, port=55555 chrome_options=options  "chrome.switches": ["window-size=1003,719"]
driver.get('http://www.google.ru')
print()
r = requests.get('http://localhost:55555/status')
r_session = requests.post('http://localhost:55555/session')
session = r_session.json()['sessionId']
r_sen = requests.post('http://localhost:55555/session/'+str(session)+'/refresh')
r_sen.json()
# 3f3d303d23e5b4e856c4d14dcd157b32
r.json()

# log("BROWSER: Chrome")
# cls.driver.get("http://dev-genie-jenkins-agent:4041")  # 'http://www.google.ru' "http://dev-genie-jenkins-agent:4041"
#cls.browser.open("http://www.google.ru") #cls.browser.open(ConfigSite()) #cls.browser.open("http://www.google.ru")


# def run_chrome(cls):
#     """Метод для запуска Chrome"""
#
#     options = webdriver.ChromeOptions()
#     #options.add_argument("--remote-debugging-port=9222")
#     options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#     options.add_argument('--allow-running-insecure-content')
#     #options.add_argument(r'--disable-web-security')
#     #options.add_argument(r"--user-data-dir=fffffffff")  # remoute77777
#     #options.add_argument(r'--test-type')
#     options.add_argument("-incognito")
#     cls.driver = webdriver.Chrome(chrome_options=options)  #
#     log("BROWSER: Chrome")


"""01. """
con = HTTPConnection("localhost:9222")
con.request("GET", "/devtools/page/76A95FDB-6D6F-4D79-85E2-C1E47E297DCC")#/json
result = con.getresponse()
result.read().decode("utf-8")
r = requests.get('http://localhost:9222/json')
r.json()
headers = {'content-type': 'application/json'}
payload = '{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}'
w = requests.get('ws://localhost:9222/devtools/page/76A95FDB-6D6F-4D79-85E2-C1E47E297DCC', params=payload)
ws = websocket.create_connection("ws://localhost:9222/devtools/page/76A95FDB-6D6F-4D79-85E2-C1E47E297DCC")
ws.send('{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}')
ws.send('{"id": 128, "method": "Page.enable"}')
result = ws.recv()
ws.send('{"id":55555555, "method":"Timeline.start","params":{"maxCallStackDepth":0, "bufferEvents":false,"liveEvents":"","includeCounters":true,"includeGPUEvents":false }}')
print("Sent")
print("Receiving...")
result2 = ws.recv()
print("Received '%s'" % result)
ws.close()
print()

