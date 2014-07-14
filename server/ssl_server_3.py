#import BaseHTTPServer, SimpleHTTPServer,
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from socketserver import ThreadingMixIn
import chardet
import time
from  urllib.parse  import  urlencode, urlparse

class MyHTTPServer(ThreadingMixIn,HTTPServer):
    def __init__(self,addr,handler):
        HTTPServer.__init__(self,addr,handler)


class MyHandler(BaseHTTPRequestHandler):

     def do_GET(self):
        try:
            print(self.path)
            dict_heders = dict((key,value) for key, value in self.headers._headers)
            print(dict_heders)
            headers2 = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
            }
            # todo: https://localhost:44444
            data2 = urlencode({'rev':"4"}, encoding="utf-8")
            self.send_response(200)  # result.status
            self.send_header("Content-type", "text/html")
            self.end_headers()
            answer = time.strftime("%H:%M:%S %d.%m.%Y")
            self.wfile.write(answer.encode("utf-8"))  # answer.encode("utf-8") f.read()
            #print(resp.decode("utf-8"))
        except   Exception:# IOError
             self.send_error(404,"File Not Found: %s" % self.path)
httpd = MyHTTPServer(("",55555), MyHandler) # фидлер послал запрос на порт https://localhost:443 и на https://localhost:55555
                                            # в браузере работает https://localhost:55555
#httpd = MyHTTPServer(("localhost",8443), MyHandler)
#httpd = HTTPServer(('localhost',8443), BaseHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='./ssl3/server.key', certfile='./ssl3/server.crt', server_side=True)#certfile=r'./ssl/server101.mycloud.pem'
httpd.serve_forever()