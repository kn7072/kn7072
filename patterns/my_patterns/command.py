# coding: utf-8
"""Паттерн команда."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Device1:
    """Класс устройства."""

    def method1(self: Device1) -> None:
        """Метод девайса - делает что-то полезное."""
        print("Делаю что-то полезное Device1")


class Device2:
    """Класс устройства."""

    def method2(self: Device2) -> None:
        """Метод девайса - делает что-то полезное."""
        print("Делаю что-то полезное Device2")


class Command(ABC):
    """Интерфейс объeкта команды."""

    @abstractmethod
    def execute() -> None:
        """Выполняет методы девайса."""
        ...


class CommandDevice1(Command):
    """Реализация команды для Device1."""

    def __init__(self: Command, device: Any) -> None:
        """Инициализирует экземпляр класса."""
        self._device = device

    def execute(self: CommandDevice1) -> None:
        """Тут вызываются методы девайса Device1."""
        self._device.method1()


class CommandDevice2(Command):
    """Реализация команды для Device2."""

    def __init__(self: Command, device: Any) -> None:
        """Инициализирует экземпляр класса."""
        self._device = device

    def execute(self: CommandDevice2) -> None:
        """Тут вызываются методы девайса Device2."""
        self._device.method2()


class Invoker:
    """Класс инициатор."""

    def set_on_start(self: Invoker, command: Command) -> Any:
        """Устанавливаем команду."""
        self._on_start = command

    def set_on_finish(self: Invoker, command: Command) -> Any:
        """Устанавливаем команду."""
        self._on_finish = command

    def do_something_important(self: Invoker) -> None:
        """Выполняет набор команд."""
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


if __name__ == "__main__":
    device1 = Device1()
    command_device1 = CommandDevice1(device1)
    device2 = Device2()
    command_object2 = CommandDevice2(device2)

    invoker = Invoker()
    invoker.set_on_start(command_device1)
    invoker.set_on_finish(command_object2)
    invoker.do_something_important()
