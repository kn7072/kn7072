# -*- coding: utf-8 -*-
from selenium import  webdriver
from browsermobproxy import Server
import json
import requests
import pymongo

conn = pymongo.Connection('localhost', 27017)
db = conn.har
coll = db.json_har

server = Server(r"d:\Python\browsermob-proxy-2.0-beta-9-bin\browsermob-proxy-2.0-beta-9\bin\browsermob-proxy",{"port":9090})
server.start()
# resp = requests.post('http://localhost:9090/proxy', {})
# port = resp.json()['port']
# resp.content
try:
    proxy = server.create_proxy()
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)
    proxy.new_har('json_har')  # .com
    driver.get('http://google.ru')
    har = proxy.har
    f = open(r'google.har', 'w')
    f.write(json.dumps(har))
    coll.save(har)
except Exception:
    f.close
    driver.quit()
    proxy.close()
    server.stop()
f.close
driver.quit()
proxy.close()
server.stop()