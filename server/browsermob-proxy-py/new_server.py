# -*- coding: utf-8 -*-
import cgi
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess


class MyHandler(BaseHTTPRequestHandler):

     def do_GET(self):

         try:
             if self.path != "/output.exe":
                 f = open(curdir+sep+"upload.html")
                 self.send_response(200)
                 self.send_header("Content-type", "text/html")
                 self.end_headers()
                 self.wfile.write(f.read())
                 f.close()
             else:
                 self.send_response(200)
                 self.send_header("Content-type", "application/octet-stream")
                 self.end_headers()
                 self.wfile.write(open(curdir+sep+"output.exe", "rb").read())
         except IOError:
             self.send_error(404,"File Not Found: %s" % self.path)

     def do_POST(self):

         try:
             ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
             if ctype == "multipart/form-data":
                 query = cgi.parse_multipart(self.rfile, pdict)
             self.send_response(200)
             self.end_headers()
             upfile = query.get("file")
             f = open(curdir+sep+"output.exe", "wb")
             f.write(upfile[0])
             f.close()
             params = " np output.exe"
             p = query.get("encryption")

             if p[0] == "aes":
                 params += " sf 1"
             elif p[0] == "rc5":
                 params += " sf 2"
             elif p[0] == "xor":
                 params += " sf 3"
             else:
                 params += " sf 0"
             p = query.get("hw_bind")
             if p[0] == "yes":
                 p = query.get("hw_bind_serial")
                 assert len(p[0]) == 8
                 params += " sn " + p[0]
             else:
                 params += " sn 0"
             p = query.get("passwd")
             assert len(p[0]) > 0
             params += " pass " + p[0]
             p = query.get("pack")
             if p[0] == "yes":
                 params += " pack 1"
             else:
                 params += " pack 0"
             pipe = subprocess.Popen("processor.exe "+params, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
             pipe.stdin.close()
             pipe.wait()
             self.wfile.write('Download results.')
         except Exception:
             pass


if __name__ == "__main__":

     try:
         server = HTTPServer(("", 8080), MyHandler)
         print("started httpserver...")
         server.serve_forever()
     except KeyboardInterrupt:
         print("^C received, shutting down server")
         server.socket.close()