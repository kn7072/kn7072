# -*- coding: utf-8 -*-
from selenium import  webdriver
from browsermobproxy import Server
from selenium.webdriver.common.proxy import *
import json
import requests

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
    'ftpProxy': None,
    'sslProxy': None,
    'noProxy': '' # set this value as desired
    })

CHROME = {
"browserName": "chrome",
        "version": "",
        "platform": "ANY",
        "javascriptEnabled": True,
        "chrome.prefs": {"profile.managed_default_content_settings.images": 2},
        "proxy": {
            "httpProxy":"localhost:"+str(port),
            "ftpProxy":None,
            "sslProxy":None,
            "noProxy":None,
            "proxyType":"MANUAL",
            "class":"org.openqa.selenium.Proxy",
            "autodetect":False
            },
        "chrome.switches": ["window-size=1003,719", "allow-running-insecure-content", "disable-web-security", "disk-cache-dir=/var/www/cake2.2.4/app/tmp/cache/selenium-chrome-cache", "no-referrers"],
        }

try:
    proxy = server.create_proxy()
    profile = webdriver.FirefoxProfile(profile_directory=r'd:\remote')
    #profile.set_proxy(proxy.selenium_proxy())
    #driver = webdriver.Firefox(proxy=proxy, firefox_profile=profile)


    ####################################################################################################################
    caps = webdriver.DesiredCapabilities.FIREFOX.copy()
    # #caps = webdriver.DesiredCapabilities.CHROME
    # # caps['chromeOptions'] = {}
    # # caps['chromeOptions']['args'] = ['enable-memory-benchmarking', 'window-size=400,400', 'window-position=200,300']
    # proxy.add_to_capabilities(caps)
    driver = webdriver.Remote(command_executor='http://192.168.1.2:4444/wd/hub', desired_capabilities=caps, proxy=proxy)
    proxy.new_har('json_har')  # .com
    driver.get('https://google.ru')
    har = proxy.har

    f = open(r'google1.har', 'a')
    f.write(json.dumps(har))

    print()

except Exception as e:
    f.close
    driver.quit()
    proxy.close()
    server.stop()
f.close
driver.quit()
proxy.close()
server.stop()