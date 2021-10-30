# coding: utf-8
"""Простой север вторая лекция. https://www.youtube.com/watch?v=g6xvW2FOuPw&list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8&index=2."""
import socket
from select import select


to_monitor = []  # список файлов(сокетов) для мониторинга - готовности для чтения
# select для мониторинга изменения состояния файловых объектов и сокетов
# nc localhost 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))  # связываем сокет с потром - создает файл сокет
server_socket.listen()  # слушем порт


def accept_connection(server_socker: socket) -> None:
    """Принимает подключения."""
    client_socket, addr = server_socket.accept()  # ожидаем подключения(блокирующая операция)-
    # событием является - во входящем буфере появятся данные о новом подключении
    print("Connection from", addr)
    #  добавим клиентский сокет в мониторинг
    to_monitor.append(client_socket)


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
        client_socket.close()


def event_loop() -> None:
    """Цикл событий."""
    while True:
        # мониторим только файлы(сокеты) - когда у них во входящих буферах появятся данные
        # первый аргумент функции select принимает список файлов для чтения(мониторим готовность для чтения)
        # второй агрумент - список файлов для записи(мониторим готовность для записи)
        # третий аргумент - ошибки
        # возвращает так же три списка - в каждом сожерщатся ожидаемые объекты
        # ready_to_read - список файлов готовых для чтения
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                # серверный сокет
                accept_connection(sock)
            else:
                # клиентский сокет
                send_message(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
