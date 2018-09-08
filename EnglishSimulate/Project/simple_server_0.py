# coding="utf-8"
from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b"hello ffffff!")

serv = HTTPServer(("localhost", 8090), HttpProcessor)
serv.serve_forever()