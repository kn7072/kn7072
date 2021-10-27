# coding: utf-8
"""Паттерн шаблоннй метод."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union


class TemplateMethodInterface(ABC):
    """Интерфейс шаблонного метода."""

    def method_1(self: TemplateMethodInterface) -> None:
        """Что-то делает."""
        print("method_1")

    def method_2(self: TemplateMethodInterface) -> None:
        """Что-то делает."""
        print("method_3")

    @abstractmethod
    def method_3(self: TemplateMethodInterface) -> None:
        """Часть алгоритма делегирующая реализацию подклассам."""
        ...

    def template_method(self: TemplateMethodInterface) -> None:
        """Шаблонный метод - скелет алгоритма."""
        self.method_1()
        self.hook()
        self.method_2()
        self.method_3()

    def hook(self: TemplateMethodInterface) -> Optional[Union[int, str]]:
        """Какое-то действие, которое можно добавить к основному алгоритму."""
        pass


class ConcreteTemplateMethod(TemplateMethodInterface):
    """Реализация интерфейса TemplateMethodInterface."""

    def method_3(self: TemplateMethodInterface) -> str:
        """Реализация метода method_3."""
        print("method_3")
        return "123"


if __name__ == "__main__":
    test_algorithm = ConcreteTemplateMethod()
    test_algorithm.template_method()
