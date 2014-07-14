import socket, ssl, time

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile=r'./ssl_key/cert.pem')  # certfile=r'./ssl_key/server.crt',keyfile=r'./ssl_key/server.key'
bindsocket = socket.socket()
bindsocket.bind(('', 44444))
bindsocket.listen(5)

# def deal_with_client(connstream):
#     data = connstream.recv(1024)
#     # empty data means the client is finished with us
#     while data:
#         if not do_something(connstream, data):
#             # we'll assume do_something returns False
#             # when we're finished with client
#             break
#         data = connstream.recv(1024)
#     #   finished with client

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        connstream.sendall(b'HTTP/1.0 200 OK\r\n')
        # client_ssl.sendall(b'Connection: Close\r\n')
        resp = time.ctime() + '\r\n'
        resp = resp.encode('latin-1')
        #client_ssl.sendall(resp.encode('latin-1'))
        connstream.sendall(b'Content-type: text/plain'+b'\r\n\r\n'+resp)
        #deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

