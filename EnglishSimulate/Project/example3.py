#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import urllib
import cgi

PORT_NUMBER = 8088


# This class will handles any incoming request from the browser
class MyHandler(BaseHTTPRequestHandler):

    error_message_format = "ERRRRRROR"

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index_example3.html"
        try:
            # Check the file extension required and
            # set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read().encode())
                f.close()

            else:
                self.send_error(200, "ERRRRRRROR")
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/send":
            self.send_response(200)
            # self.headers._headers
            self.end_headers()

            # https://stackoverflow.com/questions/42688246/do-post-method-failing-in-python-3-6
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            print("Fields value is", fields)
            res, fun = self.modeles(fields)
            # length = int(self.headers['Content-Length'])
            # post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            self.wfile.write(res)
            fun()
            return

if __name__ == "__main__":
    try:
        # Create a web server and define the handler to manage the incoming request
        server = HTTPServer(('', PORT_NUMBER), MyHandler)
        print('Started httpserver on port ', PORT_NUMBER)
        # Wait forever for incoming htto requests
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()