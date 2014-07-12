# -*- coding: utf-8 -*-
from socketserver import BaseRequestHandler
from socketserver import StreamRequestHandler, ForkingMixIn
from socketserver import TCPServer
import socket
import time

from http.server import BaseHTTPRequestHandler, HTTPServer        # Python 3
from socketserver import ThreadingMixIn
from os import curdir, sep
import cgi
# обработчик
# class ServertHandler(BaseRequestHandler):
#
#     def handle(self):
#         resp = time.ctime() + "\r\n"
#         if isinstance(self.request, socket.socket):
#             # Работа с потоком
#             self.request.sendall(resp.encode('latin-1'))
#         else:
#             # Работа с дейтаграммой
#             self.server.socket.sendto(resp.encode('latin-1'), self.client_address)
#
#
# class TimeServer(StreamRequestHandler):
#     def handle(self):
#         resp = time.ctime() + "\r\n"
#         self.wfile.write(resp.encode("latin-1"))
#
# # сервер
# class UserServer(TCPServer):  # ForkingMixIn,
#
#     address_family = socket.AF_INET
#     request_queue_size = 5
#     socket_type = socket.SOCK_STREAM
#     timeout = 2
#     allow_reuse_address = True
#     max_children = 10
#
#     def activate(self):
#         super(UserServer, self).activate(self)
#         print(dir(self.socket))
#
#
# serv2 = UserServer(('', 44444), ServertHandler)
# #serv = TCPServer(('', 44444), ServertHandler)
# serv2.serve_forever()
# print()

#/////////////////////////////////////////////////////////////////////////////
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
             if self.path == "/time.html":
                 #f = open(curdir+sep+"upload.html")
                 answer = """<!DOCTYPE html>"""
                 answer += """<html><head><title>Время</title></head><body><h1>"""
                 answer += time.strftime("%H:%M:%S %d.%m.%Y")
                 answer += """</h1></body></html>"""
                 if self.headers:
                     print(self.headers)
                     self.send_response(200)
                     self.send_header("Content-type", "text/html")
                     self.end_headers()
                     self.wfile.write(answer.encode("utf-8"))  # f.read()
                     #f.close()

             else:
                 self.send_response(200)
                 self.send_header("Content-type", "application/octet-stream")
                 self.end_headers()
                 self.wfile.write(open(curdir+sep+"output.exe", "rb").read())
         except IOError:
             self.send_error(404,"File Not Found: %s" % self.path)
     def do_POST(self):
         try:
             #
             # ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
             # if ctype == "multipart/form-data":
             #     query = cgi.parse_multipart(self.rfile, pdict)
             answer = """<!DOCTYPE html>"""
             answer += """<html><head><title>Время</title></head><body><h1>"""
             answer += time.strftime("%H:%M:%S")
             answer += """</h1></body></html>"""
             print(self.path)
             if self.path == "/time.html":
                 print(self.rfile.readline().strip())
                 print(self.headers)
                 self.send_response(200)
                 self.send_header("Content-type", "text/html")
                 self.end_headers()
                 self.wfile.write(answer.encode("utf-8"))
                 #upfile = query.get("file")
                 # f = open(curdir+sep+"output.exe", "wb")
                 # f.write(upfile[0])
                 # f.close()
                 params = " np output.exe"
                 #p = query.get("encryption")
         except IOError:
             self.send_error(404,"File Not Found: %s" % self.path)
# Пример запуска сервера
serv = MyHTTPServer(("",44444), MyHandler, '192.168.69.01')
serv.serve_forever()
#
print()