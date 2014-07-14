import socket, ssl, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(('',44444))
s.listen(5)

while True:
    client, addr = s.accept() # Принять соединение
    print ('Получен запрос на соединение с ', addr)
    client_ssl = ssl.wrap_socket(client, server_side=True, certfile=r'./ssl_key/certificate.crt', keyfile=r'./ssl_key/privateKey.key')  #certfile=r'./ssl_key/server.pem', ,  certfile=r'./ssl_key/cert.pem' keyfile=r'./ssl_key/server.key'
    print("dddddddd")
    client_ssl.sendall(b'HTTP/1.0 200 OK\r\n')
    # client_ssl.sendall(b'Connection: Close\r\n')
    resp = time.ctime() + '\r\n'
    resp = resp.encode('latin-1')
    #client_ssl.sendall(resp.encode('latin-1'))
    client_ssl.sendall(b'Content-type: text/plain'+b"\r\n" +b"\r\n"+resp)
    client_ssl.close()
    client.close()
# https://localhost:44444/

# import BaseHTTPServer, SimpleHTTPServer, ssl
#
# httpd = BaseHTTPServer.HTTPServer(('localhost', 8443), SimpleHTTPServer.SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server101.mycloud.pem', server_side=True)
# httpd.serve_forever()
# скопируем клуч и сертификат в один файл
# cat server101.mycloud.key server101.mycloud.crt > server101.mycloud.pem
# # запустим сервер на питоне
# python myserver.py