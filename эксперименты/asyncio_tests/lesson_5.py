# coding: utf-8
"""Простой север - на генераторах - Лекция 5 https://www.youtube.com/watch?v=hOP9bKeDOHs&list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8&index=5."""
from __future__ import annotations

import socket
from select import select


tasks = []  # список генераторов - должна быть очередь
to_read = {}  # ключ - сокет, значение - генератор
to_write = {}  # ключ - сокет, значение - генератор


def server() -> None:
    """Сервер."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    while True:
        yield ("read", server_socket)
        client_socket, addr = server_socket.accept()  # read
        print("Connection from", addr)
        tasks.append(client(client_socket))


def client(client_socket: socket.socket) -> None:
    """Слиент."""
    while True:
        yield ("read", client_socket)
        request = client_socket.recv(4096)  # read
        print(request.decode())
        if request:
            response = "Hello word\n".encode()
            yield ("write", client_socket)
            client_socket.send(response)  # write
        else:
            break
    print("Outside inner while loop")
    client_socket.close()


def event_loop() -> None:
    """Цикл событий."""
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == "read":
                to_read[sock] = task
            if reason == "write":
                to_write[sock] = task
        except StopIteration:
            print("Done")        


tasks.append(server())
event_loop()