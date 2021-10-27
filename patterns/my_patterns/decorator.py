# coding: utf-8
"""Паттерн декоратор."""
from __future__ import annotations


class Component:
    """Класс - который будет расширен."""

    def do_something_useful(self: Component) -> int:
        """Делаем что-то полезное."""
        print("Делаем что-то полезное Component.")
        return 2


class Decorator(Component):
    """Еще один декоратор."""

    def __init__(self: Component, component: Component) -> None:
        """Инициализирует экземпляр класса."""
        self._component = component

    def do_something_useful(self: Component) -> int:
        """Делаем что-то полезное."""
        print("Делаем что-то полезное Decorator.")
        return 1 + self._component.do_something_useful()


if __name__ == "__main__":
    object_decorator_1 = Component()
    object_decorator_2 = Decorator(parent_decorator=object_decorator_1)
    result = object_decorator_2.do_something_useful()
    print(result)
