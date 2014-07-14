# -*-coding utf-8 -*-
import socket, ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('translate.google.ru',443))  # gmail.google.com
print(ssl_s.cipher())
# Отправить запрос
ssl_s.write(b'GET / HTTP/1.0\r\n\r\n')
print()
