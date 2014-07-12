# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import socket

host = "localhost"
port = 44444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
test = ['one', 'two', 'exit', 'ssssss']

for x in test:
    buf = x.encode("utf-8")
    s.send(buf)
    s.settimeout(2)  # установка таймаута
    result = s.recv(1024) # получение данных
    print(result)
s.close()
# buf = "exit"  # raw_input(">>")
# #buf = pickle.dumps(buf)
# buf = buf.encode("utf-8")
# s.send(buf)
# result = s.recv(1024)
# print (result)
# if buf == "exit":
#     break

# Думаю, что все понятно, т.к. все уже разбиралось ранее. Единственное новое здесь — это метод connect, с помощью
# которого мы подключаемся к серверу. Дальше мы читаем 1024 байт данных и закрываем сокет.