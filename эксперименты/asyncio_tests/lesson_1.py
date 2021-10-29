# coding: utf-8
"""Простой север."""
import socket


# nc localhost 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))  # связываем сокет с потром
server_socket.listen()  # слушем порт

while True:
    print("Before .accept()")
    client_socket, addr = server_socket.accept()  # ожидаем подключения(блокирующая операция)
    print("Connection from", addr)

    while True:
        # сервер способен работать только для одного подключения,
        # из этого цикла не выйдем до тех пор, пока клинет не отключится
        request = client_socket.recv(4096)  # получаем запрос от клиента
        print(request.decode())
        if request:
            response = "Hello word\n".encode()
            client_socket.send(response)  # отвечаем клиенту
        else:
            break
    print("Outside inner while loop")
    client_socket.close()
