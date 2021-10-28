# coding: utf-8
"""Паттерн адаптер."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Target(ABC):
    """Интерфейс целевого объекта."""

    @abstractmethod
    def method_1(self: Target) -> None:
        """Что-то делает method_1."""
        ...

    @abstractmethod
    def method_2(self: Target) -> None:
        """Что-то делает method_1."""
        ...


class Adaptee:
    """Объект, интерфейс которого не известен клиентскому коду."""

    def method_adaptee_1(self: Adaptee) -> None:
        """Что-то делает method_adaptee_1."""
        print("Adaptee.method_adaptee_1")

    def method_adaptee_2(self: Adaptee) -> None:
        """Что-то делает method_adaptee_2."""
        print("Adaptee.method_adaptee_2")


class Adapter(Target):
    """Объект, заменяющий целевой объект."""

    def __init__(self: Adapter, target_object: Adaptee) -> None:
        """Инициализаця экземпляра."""
        self._target_object = target_object

    def method_1(self: Adapter) -> None:
        """Эмитирует поведение Target."""
        self._target_object.method_adaptee_1()

    def method_2(self: Adapter) -> None:
        """Эмитирует поведение Target."""
        self._target_object.method_adaptee_1()
        self._target_object.method_adaptee_2()


if __name__ == "__main__":
    adaptee_object = Adaptee()
    adapter_object = Adapter(adaptee_object)
    adapter_object.method_1()
    adapter_object.method_2()
