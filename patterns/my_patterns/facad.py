# coding: utf-8
"""Паттерн фасад."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Subsystem1:
    """Устройсто."""

    def on(self: Subsystem1) -> None:
        """Включает устройсто."""
        print("Включили устройство Subsystem1.")

    def off(self: Subsystem1) -> None:
        """Выключает устройсто."""
        print("Выключили устройство Subsystem1.")

    def do_something(self: Subsystem1) -> None:
        """Делает что-то полезное."""
        print("Сделал что-то полезное Subsystem1.")


class Subsystem2:
    """Устройсто."""

    def on(self: Subsystem2) -> None:
        """Включает устройсто."""
        print("Включили устройство Subsystem2.")

    def off(self: Subsystem2) -> None:
        """Выключает устройсто."""
        print("Выключили устройство Subsystem2.")

    def do_something(self: Subsystem2) -> None:
        """Делает что-то полезное."""
        print("Сделал что-то полезное Subsystem2.")


class Facad(ABC):
    """Интерфейс фасад."""

    def __init__(self: Facad, subsystem1: Subsystem1, subsystem2: Subsystem2) -> None:
        """Инициирует экземпляр."""
        self._subsistem1 = subsystem1
        self._subsistem2 = subsystem2

    def on_all(self: Facad) -> None:
        """Включает все устроийства."""
        self._subsistem1.on()
        self._subsistem2.on()

    def off_all(self: Facad) -> None:
        """Выключает все устроийства."""
        self._subsistem1.do_something()
        self._subsistem1.off()
        self._subsistem2.do_something()
        self._subsistem2.off()


if __name__ == "__main__":
    subsystem1 = Subsystem1()
    subsystem2 = Subsystem2()
    facad = Facad(subsystem1, subsystem2)
    facad.on_all()
    facad.off_all()
