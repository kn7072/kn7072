# coding: utf-8
"""Простой север - на колбэках - Лекция 3 https://www.youtube.com/watch?v=ikKGMp4jb_o&list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8&index=5."""
import selectors
import socket

from __future__ import annotations
from typing import List, Tuple


# python3 selectors.DefaultSelector() чтобы узнать функцию по умолчанию
# для мониторинга файлов(зависит от операционной системы)
# nc localhost 5000
selector = selectors.DefaultSelector()


def server() -> None:
    """Сервер."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))  # связываем сокет с потром
    server_socket.listen()  # слушем порт
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socker: socket) -> None:
    """Принимает подключения."""
    client_socket, addr = server_socker.accept()  # ожидаем подключения(блокирующая операция)-
    # событием является - во входящем буфере появятся данные о новом подключении
    print("Connection from", addr)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket: socket) -> None:
    """Принимает запрос от клиента и отвечает на него."""
    request = client_socket.recv(4096)  # получаем запрос от клиента
    # событием является - появление данных от пользователся во входящем буфере
    print(request.decode())
    if request:
        response = "Hello word\n".encode()
        client_socket.send(response)  # отвечаем клиенту
        # событием является - очистка буфера, так как идет чтение из буфера
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop() -> None:
    """Цикл событий."""
    while True:
        events: List[Tuple["SelectorKey", "_EventMask"]] = selector.select()  # (key, events)
        # key - именованный кортеж с ключами как при вызове register(fileobj, events, data)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    event_loop()    
