# -*- coding: utf-8 -*-
from selenium import  webdriver
from browsermobproxy_a import Server
import json
import requests
#import pymongo

# conn = pymongo.Connection('localhost', 27017)
# db = conn.har
# coll = db.json_har

myProxy = "host:8080"
server = Server(r"d:\Python\browsermob-proxy-2.0-beta-9-bin\browsermob-proxy-2.0-beta-9\bin\browsermob-proxy",{"port":9090})
server.start()
from selenium.webdriver.common.proxy import *
resp = requests.post('http://localhost:9090/proxy', {})
port = resp.json()['port']
# resp.content
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': port,
    'ftpProxy': port,
    'sslProxy': port,
    'noProxy': '' # set this value as desired
    })
try:
    #proxy = server.create_proxy()
    #profile = webdriver.FirefoxProfile(profile_directory=r'd:\remote')
    #profile.set_proxy(proxy.selenium_proxy())
    #driver = webdriver.Firefox(proxy=proxy, firefox_profile=profile)  # firefox_profile=profile
    ####################################################################################################################
    #caps = webdriver.DesiredCapabilities.FIREFOX.copy()

    caps = webdriver.DesiredCapabilities.CHROME
    #proxy.add_to_capabilities(caps)
    # http://docs.seleniumhq.org/docs/04_webdriver_advanced.jsp
    driver = webdriver.Remote(command_executor='http://192.168.1.2:4444/wd/hub', desired_capabilities=caps)
    proxy.new_har('json_har')  # .com
    driver.get('http://google.ru')
    har = proxy.har
    f = open(r'google1.har', 'a')
    f.write(json.dumps(har))
    print()
    #coll.save(har)
except Exception as e:
    f.close
    driver.quit()
    proxy.close()
    server.stop()
f.close
driver.quit()
proxy.close()
server.stop()