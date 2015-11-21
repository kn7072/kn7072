# -*- coding:utf-8 -*-
import requests
import http.client
url = r'https://www.google.ru'
proxies = {
  "http": "127.0.0.1:8888",
  "https": "127.0.0.1:8888",
}
req = requests.get(url, proxies=proxies, verify=False)#

conn = http.client.HTTPSConnection("127.0.0.1", 8888)
conn.set_tunnel("www.google.ru")
x = conn.request("GET","/index.html")
req = req.prepare()
s = requests.Session()