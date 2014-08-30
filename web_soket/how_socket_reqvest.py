# -*- coding:utf-8 -*-
import requests
import websocket
import socket
from http.client import HTTPConnection, HTTPSConnection, OK

headers = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Sec-WebSocket-Version": "13",
           "Host": "localhost:9222",
           "Upgrade": "WebSocket",
           "Connection": "Upgrade",
           "Sec-WebSocket-Key":"VGE8qy2/Z8WdXh9XxOgHvA=="
          }
res = requests.get('http://localhost:9222/devtools/page/AF01B6DF-48A5-4DC3-877E-508C967F60C1', headers=headers)
print(res.headers)
res.connection.send('{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}')
# ws.send('{"id": 123,"method": "Page.reload","params": {"ignoreCache": true}}')
print(res.status)
print()