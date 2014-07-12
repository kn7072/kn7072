# -*- coding: utf-8 -*-
import time
import socket
from  urllib.parse  import  urlencode
from http.client import HTTPConnection

# Запустите его и наберите в браузере адрес http://localhost:8080/time.html
def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
    data = data.encode("utf-8")
    conn.sendall(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
    conn.sendall(b"Server: simplehttp\r\n")
    conn.sendall(b"Connection: close\r\n")
    conn.sendall(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.sendall(b"Content-Length: " + bytes(len(data)) + b"\r\n" +b"\r\n"+data)
    # conn.sendall(b"\r\n")  # после пустой строки в HTTP начинаются данные
    # conn.sendall(data)

    headers = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
               "Accept": "*/*",
               "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "close",
               "Server": "simplehttp",
               "Content-Type":"text/plain; charset=utf-8"
              }

def parse(conn, addr):  # обработка соединения в отдельной функции
    data = b""
    while not b"\r\n" in data:  # ждём первую строку
        tmp = conn.recv(1024)
        if not tmp:  # сокет закрыли, пустой объект
            break
        else:
            data += tmp
    if not data:  # данные не пришли
        return  # не обрабатываем
    udata = data.decode("utf-8")
    print(udata)
    # берём только первую строку
    udata = udata.split("\r\n", 1)[0]
    print(udata)
    # разбиваем по пробелам нашу строку
    method, address, protocol = udata.split(" ", 2)

    if method != "GET" or address != "/time.html":
        send_answer(conn, "404 Not Found", data="Не найдено")
        return

    answer = """<!DOCTYPE html>"""
    answer += """<html><head><title>Время</title></head><body><h1>"""
    answer += time.strftime("%H:%M:%S %d.%m.%Y")
    answer += """</h1></body></html>"""

    send_answer(conn, typ="text/html; charset=utf-8", data=answer)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 44444))
sock.listen(5)

try:
    while 1:  # работаем постоянно
        conn, addr = sock.accept()
        print("New connection from " + addr[0] +" "+ str(sock.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN)))
        try:
            parse(conn, addr)
        except:
            send_answer(conn, "500 Internal Server Error", data="Ошибка")
        finally:
            # так при любой ошибке
            # сокет закроем корректно
            conn.close()
finally: sock.close()
# так при возникновении любой ошибки сокет
# всегда закроется корректно и будет всё хорошо
# sock.send( open("file.jpg", "rb").read() )  # отправка изображений
# fp = open("file.jpg", "wb")  # так можно принять изображение
# while 1:
#     data = sock.read(4096)
#     if not data: break
#     fp.write(data)
# fp.close()