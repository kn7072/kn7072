# coding: utf-8
"""Паттерн цепочка обязанностей."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class Const(Enum):
    """Константы."""

    A = "A"
    B = "B"
    C = "C"


class Handler(ABC):
    """Интерфейс обработчика."""

    @abstractmethod
    def set_next_handler(self: Handler, handler: Handler) -> Handler:
        """Устанавливает обработчик."""
        ...

    @abstractmethod
    def handle(self: Handler, request: str) -> None:
        """Принимает запрос."""
        ...


class BaseHandle(Handler):
    """Базовый класс обработчика."""

    _next_handler = None

    def set_next_handler(self: Handler, handler: Handler) -> Handler:
        """Устанавливает обработчик."""
        self._next_handler = handler
        return handler

    def handle(self: BaseHandle, request: str) -> None:
        """Принимает запрос."""
        if self._next_handler:
            # делегирует выполнение
            self._next_handler.handle(request)


class ConcreteHandleA(BaseHandle):
    """Конкретный обработчик - использующий базовый класс чтобы не дублировать базовые методы."""

    def handle(self: ConcreteHandleA, request: str) -> None:
        """Принимает запрос."""
        if request == Const.A:
            # можем обработать
            print("Обработчик ConcreteHandleA")
        else:
            # делегирует выполнение
            super().handle(request)


class ConcreteHandleB(BaseHandle):
    """Конкретный обработчик - использующий базовый класс чтобы не дублировать базовые методы."""

    def handle(self: ConcreteHandleB, request: str) -> None:
        """Принимает запрос."""
        if request == Const.B:
            # можем обработать
            print("Обработчик ConcreteHandleB")
        # даже если обработали запроса все равно делегирует выполнение
        super().handle(request)


class ConcreteHandleС(BaseHandle):
    """Конкретный обработчик - использующий базовый класс чтобы не дублировать базовые методы."""

    def handle(self: ConcreteHandleС, request: str) -> None:
        """Принимает запрос."""
        if request == Const.C:
            # можем обработать
            print("Обработчик ConcreteHandleС")
        else:
            # делегирует выполнение
            super().handle(request)


if __name__ == "__main__":
    handler_0 = ConcreteHandleA()
    handler_1 = ConcreteHandleB()
    handler_2 = ConcreteHandleС()
    handler_0.set_next_handler(handler_1).set_next_handler(handler_2)
    handler_0.handle(Const.C)
