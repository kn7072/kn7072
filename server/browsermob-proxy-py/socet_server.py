# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Сервер
import pickle
import time
import socket

host = "localhost"
port = 44444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
sock, addr = s.accept()
time_end = time.time() + 120
i=0
while True:
    buf = sock.recv(1024) # получение данных
    #buf = pickle.loads(buf)
    buf = buf.decode("utf-8")
    if time.time() > time_end:
         print("не дождались данных")
         break
    if buf == "exit":
        sock.send("bye_ddddd".encode("utf-8"))
        break
    elif buf:
        sock.send(buf.encode("utf-8"))
sock.close()
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # порт возьмем любой от нуля до 65535
# sock.bind(('', 9090))
# # этот параметр определяет размер очереди
# sock.listen(1)
# # возвращает кортеж с двумя элементами: новый сокет и адрес клиента. Именно этот сокет и будет использоваться
# # для приема и посылке клиенту данных.
# conn, addr = sock.accept()
# print('connected:', addr)
# # Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента принимает количество байт для
# # чтения. Мы будем читать порциями по 1024 байт (или 1 кб):
# time_end = time.time() + 120
# while True:
#     data = conn.recv(1024)
#     if time.time() > time_end:
#         print("не дождались данных")
#         break
#     if not data:
#         break
#     conn.send(data.upper())
#
# conn.close()

# data = conn.recv(1024).split("\r\n")        # считываем запрос и бьём на строки
# method, url, proto = data[0].split(" ", 2)  # обрабатываем первую строку
#
# headers = {}
# for pos, line in enumerate(data[1:]):  # проходим по строкам и заодно запоминаем позицию
#     if not line.strip():               # пустая строка = конец заголовков, начало тела**
#         break
#     key, value = line.split(": ", 1)   # разбираем строку с заголовком
#     headers[key.upper] = value       # приводим ключ к "нормальному" виду чтобы обращение было регистронезависимым
#
# # всё остальное - тело** запроса
# body = "\r\n".join(data[pos])</pos></key.upper>
# Собственно сервер готов. Он принимает соединение, принимает от клиента данные, возвращает их в виде строки в верхнем
# регистре и закрывает соединение. Все просто :)