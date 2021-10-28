# coding: utf-8
"""Паттерт заместитель."""
from __future__ import annotations

from abc import ABC, abstractmethod


class ClientObjectBase(ABC):
    """Интерфейс объекта, знакомого клинтскому коду."""

    @abstractmethod
    def method_1(self: ClientObjectBase) -> None:
        """Что-то делаю."""
        ...

    @abstractmethod
    def method_2(self: ClientObjectBase) -> None:
        """Что-то делаю 2."""
        ...


class ClientObject(ClientObjectBase):
    """Целевой клиенский объект."""

    def method_1(self: ClientObjectBase) -> None:
        """Что-то делаю."""
        print("ClientObject - method_1")

    def method_2(self: ClientObjectBase) -> None:
        """Что-то делаю 2."""
        print("ClientObject - method_2")


class Proxy(ClientObjectBase):
    """Объект заместителя."""

    def __init__(self: Proxy, client_object: ClientObjectBase = None) -> None:
        """Инициализация объекта."""
        super().__init__()
        self._client_object = client_object if client_object else ClientObject()

    def method_1(self: Proxy) -> None:
        """Делаю что-то полезное и вызываю метод целевого объекта."""
        print("Proxy method_1")
        self._client_object.method_1()

    def method_2(self: Proxy) -> None:
        """Делаю что-то полезное и вызываю метод целевого объекта."""
        print("Proxy method_2")
        self._client_object.method_2()


if __name__ == "__main__":
    proxy_object = Proxy()
    proxy_object.method_1()
    proxy_object.method_2()
