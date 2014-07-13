# -*- coding: utf-8 -*-
from socketserver import BaseRequestHandler
from socketserver import StreamRequestHandler, ForkingMixIn
from socketserver import TCPServer
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer        # Python 3
from http.client import HTTPConnection, HTTPException
from socketserver import ThreadingMixIn
from  urllib.parse  import  urlencode, urlparse
import chardet
from os import curdir, sep

class MyHTTPServer(ThreadingMixIn,HTTPServer):
    def __init__(self,addr,handler,subnet):
        HTTPServer.__init__(self,addr,handler)
        self.subnet = subnet
    # def verify_request(self, request, client_address):
    #     host, port = client_address
    #     if not host.startswith(self.subnet):
    #         return False
    #     return HTTPServer.verify_request(self,request,client_address)
# localhost:44444/time.html
class MyHandler(BaseHTTPRequestHandler):

     def do_GET(self):
         try:
             #print(self.headers.__dict__)
             print(self.path)
             dict_heders = dict((key,value) for key, value in self.headers._headers)
             print(dict_heders)
             headers2 = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
             "Accept": "*/*",
             "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
             "Accept-Encoding": "gzip, deflate",
             #"Referer": "http://finviz.com/quote.ashx?t=ABT&ty=c&ta=1&p=d&b=1",
             "Connection": "keep-alive"
             }
             # todo: http://www.finviz.com/screener.ashx?v=340&s=ta_topgainers
             data2 = urlencode({'rev':"4"}, encoding="utf-8")
             if dict_heders['Host'] != 'localhost:44444':
                 r = urlparse(self.path)
                 print(r.scheme, r.netloc, r.path)
                 con2 = HTTPConnection(dict_heders['Host'])  # "finviz.com" dict_heders['Host']
                 print(dict_heders['Host'], self.path)
                 path = chardet.detect(bytes(self.path, "utf-8"))
                 #dict_heders_ = urlencode(dict_heders, encoding="utf-8")
                 print(dict_heders)  # r.path+'?'+r.query,
                 con2.request("GET",r.path+'?'+r.query, headers=dict_heders)  # "/script/quote.js?%s" % data2, headers=headers2
                 #con2.request("GET", self.path,  headers=headers2)
                 result = con2.getresponse()
                 headers = result.getheaders()
                 print(headers)
                 print("/////////////result.reason//////////////////")
                 print(result.reason)
                 coding = result.msg.get_content_charset()
                 resp = result.read()
                 #print("dddd"+resp.decode("utf-8"))
                 print(result.status)
                 con2.close()
                 # todo: создаю исключение
                 #raise HTTPException
                 self.send_response(result.status)  # result.status
                 for key, value in headers:
                    self.send_header(key, value)
                 self.end_headers()
                 self.wfile.write(resp)  # answer.encode("utf-8") f.read()
             else:
                 self.send_response(200)  # result.status
                 self.send_header("Content-type", "text/html")
                 self.end_headers()
                 answer = time.strftime("%H:%M:%S %d.%m.%Y")
                 self.wfile.write(answer.encode("utf-8"))  # answer.encode("utf-8") f.read()
                 #print(resp.decode("utf-8"))
         except   Exception:# IOError
             self.send_error(404,"File Not Found: %s" % self.path)
     # def log_error(self, format, *args):
     #     print(args, format, "fdfdfdffsdfdsf")
     def do_POST(self):
         try:
             print(self.path)
             if self.path == "/time.html":
                 print(self.rfile.readline().strip())
                 print(self.headers)
                 self.send_response(200)
                 self.send_header("Content-type", "text/html")
                 self.end_headers()
                 answer = time.strftime("%H:%M:%S %d.%m.%Y")
                 self.wfile.write(answer.encode("utf-8"))
                 #self.wfile.write(answer.encode("utf-8"))

         except IOError:
             self.send_error(404,"File Not Found: %s" % self.path)
# Пример запуска сервера
serv = MyHTTPServer(("",44444), MyHandler, '192.168.69.01')
serv.serve_forever()
# localhost:44444/time.html
print()