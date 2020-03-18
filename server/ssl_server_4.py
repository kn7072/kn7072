'''
SimpleSecureHTTPServer.py - simple HTTP server supporting SSL.

- replace fpem with the location of your .pem server file.
- the default port is 443.

usage: python SimpleSecureHTTPServer.py
'''
import socket, os
#from SocketServer import BaseServer
from http.server import BaseHTTPRequestHandler, HTTPServer
#from BaseHTTPServer import HTTPServer
#from SimpleHTTPServer import SimpleHTTPRequestHandler
# from OpenSSL import SSL
import ssl as SSL

# http://code.activestate.com/recipes/442473-simple-http-server-supporting-ssl-secure-communica/
# openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        #BaseServer.__init__(self, server_address, HandlerClass)
        HTTPServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.PROTOCOL_SSLv23)  # ContextSSL.SSLv23_METHOD
        #server.pem's location (containing the server private key and
        #the server certificate).
        fpem = './ssl/server.pem'
        ctx.use_privatekey_file (fpem)
        ctx.use_certificate_file(fpem)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        #self.socket = SSL.wrap_socket (self.socket,  certfile=fpem, server_side=True)
        self.server_bind()
        self.server_activate()


class SecureHTTPRequestHandler(BaseHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    server_address = ('', 443) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print ("Serving HTTPS on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()

#  IF EXIST node.pid (for /F %%i in (node.pid) do taskkill /F /T /PID %%i)
if __name__ == '__main__':
    test()