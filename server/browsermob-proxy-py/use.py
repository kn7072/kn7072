#from browsermobproxy import Server
#from browsermobproxy import client
from browsermobproxy.server import Server
import requests

server = Server(r"d:\Python\browsermob-proxy-2.0-beta-9-bin\browsermob-proxy-2.0-beta-9\bin\browsermob-proxy",{"port":9090})
server.start()
resp = requests.post('http://localhost:9090/proxy', {})
resp
resp.content
port = resp.json()['port']  # Ну а теперь просто надо открыть какой-то браузер и настроить на работу через прокси host = localhost и port = 9091
# http://localhost:9090/proxy/9091/har
resp = requests.put('http://localhost:9090/proxy/9091/har', {"initialPageRef": "google"})
# Далее идем в браузер с прокси и открываем урл http://google.com
# Через прокси прошли уже данные, теперь нам надо считать их. Как это можно сделать?
resp = requests.get('http://localhost:9090/proxy/9091/har')
resp.content
s = resp.json()
print('s')