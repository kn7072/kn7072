# -*-coding utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request as rec
import urllib.error as error
import ssl, time
from socketserver import BaseRequestHandler , StreamRequestHandler, TCPServer
import socket

site = r'http://finviz.com'
site_2 = r'https://translate.google.ru'  # /?hl=ru&tab=wT#en/ru/amend

class MyHTTPSServer(HTTPServer):
    allow_reuse_address = True  # 615

    def __init__(self, addr, handler):
        HTTPServer.__init__(self, addr, handler)

    # def verify_request(self, request, client_address):
    #     host, port = client_address
    #     if not host.startswith(self.subnet):
    #         return False
    #     return HTTPServer.verify_request(self,request,client_address)

class MyHandler(StreamRequestHandler):  # BaseHTTPRequestHandler
     def handle(self):
        resp = time.ctime() + '\r\n'
        if isinstance(self.request,socket.socket):
            print("Работа с потоком")  # encode(encoding='utf-8')  .decode("utf-8")
            try:
                self.request.sendall(resp.encode('utf-8'))
            except Exception as e:
                print(e)
        else:
            print("Работа с дейтаграммой")
            self.server.socket.sendto(resp.encode('latin-1'), self.client_address)

        print(self.client_address)
        self.wfile.write(resp.encode('utf-8'))
        pass

server = MyHTTPSServer(('', 44444), MyHandler)  # TCPServer
#server.socket = ssl.wrap_socket(server.socket, keyfile='my_key.key', certfile='my_cert.crt', server_side=True)
server.serve_forever()
print()
# try:
#     # u = rec.urlopen(r'https://translate.google.ru')
#     buid = rec.build_opener()
#     rec.install_opener(buid)
#     #u = rec.Request(site_2)
#     # u.type
#     #u.get_method()
#     #data = u.read()
#     buid.open(site_2)
#
#
#     print("dd")
# except error.HTTPError as e:
#     print(e)