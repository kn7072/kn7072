import time
import socket
import json
from  urllib.parse  import  urlencode
from http.client import HTTPConnection
#//////////////////////////////////////////////////////
data = urlencode({'s':"m"}, encoding="utf-8")
headers = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Accept": "*/*",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "keep-alive"
          }
host = "localhost"
port = 44444
con = HTTPConnection("localhost:44444")
con.request("GET", "/time.html",  headers=headers)# ?%s % data
result = con.getresponse()  # Экземпляр  класса  HTTPResponse
cod = result.msg.get_content_charset()
print(result.status)
print(result.getheader("Content-Type"))
print(result.read().decode("utf-8"))
con.close()
#//////////////////////////////////////////////////////
# import requests  
# payload = {'key1': 'value1', 'key2': 'value2'}
# data = urlencode({'s':"m", 'ty':'c', 'p':'d', 't':'A'}, encoding="utf-8")
# r = requests.get(r"http://localhost:44444/time.html", stream=True)#, params=payload
# print(r.url)
#////////////////////ниже рабочий код///////////////////////
# conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conn.connect((host, port))
# conn.send(b"Hello! \n")
# # data = b""
# # tmp = conn.recv(1024)
# # time_end = time.time() + 120
# # while tmp:
# #     if time.time() > time_end:
# #          print("не дождались данных")
# #          break
# #     data += tmp
# #     tmp = conn.recv(1024)
# #     print(tmp)
# # print(data.decode("utf-8"))
# conn.close()