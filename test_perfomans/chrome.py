# -*- coding:utf-8 -*-
from selenium import webdriver
import websocket
import socket
from http.client import HTTPConnection, HTTPSConnection, OK
#from config_site import ConfigSite
import requests
import socket, struct, hashlib, threading, cgi
options = webdriver.ChromeOptions()
#options.add_argument(r"--remote-debugging-port=9222")
#options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#options.add_argument('--allow-running-insecure-content')
#options.add_argument("--verbose")
#options.add_argument(r'--disable-web-security')
options.add_argument(r"--user-data-dir=D:\prof2\chrome2\xxx")  # remoute77777  D:\chome_prof
#driver = webdriver.Chrome(chrome_options=options)
from  urllib.parse  import  urlencode
from http.client import HTTPConnection
websocket.enableTrace(True)


def decode_key (key):
    num = ""
    spaces = 0
    for c in key:
        if c.isdigit(): num += c
        if c.isspace():
            spaces += 1
    return int(num) / spaces

def create_hash (key1, key2, code):
	a = struct.pack(">L", decode_key(key1))
	b = struct.pack(">L", decode_key(key2))
	md5 = hashlib.md5(a + b + code)
	return md5.digest()

#print("Sending 'Hello, World'...")
#con = HTTPConnection("localhost:9222")
# con.request("GET", "/json")
# result = con.getresponse()
# result.read().decode("utf-8")

host = "localhost"
port = 9222

data = urlencode({"id": 123,"method": "Page.reload","params": {"ignoreCache": 'true'}}, encoding="utf-8")
headers = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Accept": "*/*",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "keep-alive"
          }
# host = "localhost"
# port = 44444
#con = HTTPConnection("localhost:44444")
#con.request("GET", "/time.html",  headers=headers)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
shake = "GET /devtools/page/4D6AFFDE-1A07-4FBF-919D-5B712A83378D HTTP/1.1\r\n"
shake += "User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36\r\n"
shake +=   "Pragma: no-cache\r\n"
shake +=   "Cache-Control: no-cache\r\n"
shake +=   "Origin: chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo\r\n"
shake +=   "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits, x-webkit-deflate-frame\r\n"
shake +=   "Sec-WebSocket-Key: tKPRIb+78i1mJdpyejFn9Q==\r\n"
shake +=   "Sec-WebSocket-Version: 13\r\n"
shake +=   "Host: localhost:9222\r\n"
shake +=   "Connection: Upgrade\r\n"
shake +=   "Upgrade: websocket\r\n\r\n"

# shake += "Origin: chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo\r\n"
# shake += "WebSocket-Location: ws://localhost:9222/devtools/page/3ECD7214-C336-4313-84C4-2070A9CCFCFF\r\n"
# shake += "WebSocket-Protocol: sample\r\n\r\n"
# shake += "Sec-WebSocket-Origin: %s\r\n" % ('http://localhost:9222/devtools/page/3ECD7214-C336-4313-84C4-2070A9CCFCFF')
# shake += "Sec-WebSocket-Location: ws://%s\r\n" % ('localhost:9222/devtools/page/3ECD7214-C336-4313-84C4-2070A9CCFCFF')
r='{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}'
#shake += "Sec-WebSocket-Protocol: sample\r\n\r\n"
s.sendall(shake.encode("utf-8"))
result = s.recv(1024)
s.send('{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}\r\n'.encode("utf-8"))
print(result)
result2 = s.recv(1024)
print(result2)
print()
#s.send(buf)

# r = requests.get('http://localhost:9222/json')
# r.json()

headers_socket = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
                  "Pragma": "no-cache",
                  "Cache-Control": "no-cache",
                  "Origin": "chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo",
                  "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits, x-webkit-deflate-frame",
                  "Sec-WebSocket-Key": "tKPRIb+78i1mJdpyejFn9Q==",
                  "Sec-WebSocket-Version": "13",
                  "Host": "localhost:9222",
                  "Connection": "Upgrade",
                  "Upgrade": "websocket"
          }

# con = HTTPConnection("localhost:9222")
# con.request("GET", "/devtools/page/4D6AFFDE-1A07-4FBF-919D-5B712A83378D",  headers=headers_socket)
# result = con.getresponse()
# print(result.status)
# x = con.send(b'{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}' + b"\r\n" +b"\r\n")

ws = websocket.create_connection("ws://localhost:9222/devtools/page/3ECD7214-C336-4313-84C4-2070A9CCFCFF")
ws.send('{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}')
print("Sent")
print("Receiving...")
result = ws.recv()
print("Received '%s'" % result)
ws.close()
print()


# http://localhost:9222/devtools/page/3ECD7214-C336-4313-84C4-2070A9CCFCFF
# Upgrade: websocket
# Connection: Upgrade
# Host: localhost:9222
# Origin: http://localhost:9222
# Sec-WebSocket-Key: BnpnN606RP6IsuLFZtO55w==
# Sec-WebSocket-Version: 13
