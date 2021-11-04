# coding: utf-8
"""Паттерт фабричный метод."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Product(ABC):
    """Объект с которым будет работать Creator."""

    @abstractmethod
    def do_something_a(self: Product) -> None:
        """Что-то делает."""
        ...

    @abstractmethod
    def do_something_b(self: Product) -> None:
        """Что-то делает."""
        ...


class ConcreteProductA(Product):
    """Реализация продукта."""

    def do_something_a(self: Product) -> None:
        """Что-то делает."""
        print("Сделал что-то полезное ConcreteProductA.do_something_a")

    @abstractmethod
    def do_something_b(self: Product) -> None:
        """Что-то делает."""
        print("Сделал что-то полезное ConcreteProductA.do_something_b")


class ConcreteProductB(Product):
    """Реализация продукта."""

    def do_something_a(self: Product) -> None:
        """Что-то делает."""
        print("Сделал что-то полезное ConcreteProductB.do_something_a")

    @abstractmethod
    def do_something_b(self: Product) -> None:
        """Что-то делает."""
        print("Сделал что-то полезное ConcreteProductB.do_something_b")


class Creator(ABC):
    """Предоставляет объект Product."""

    @abstractmethod
    def create(self: Creator) -> Product:
        """Предоставляем подклассам создавать конкретный продукт."""
        ...

    def do_something(self: Creator) -> None:
        """Делает что-то полезное."""
        product = self.create()
        product.do_something_a()
        product.do_something_b()


class CreatorA(Creator):
    """Реализация Creator."""

    def create(self: Creator) -> Product:
        """Предоставляем подклассам создавать конкретный продукт."""
        return ConcreteProductA()


class CreatorB(Creator):
    """Реализация Creator."""

    def create(self: Creator) -> Product:
        """Предоставляем подклассам создавать конкретный продукт."""
        return ConcreteProductB()


if __name__ == "__main__":
    creator_a = CreatorA()
    creator_a.do_something()

    creator_b = CreatorB()
    creator_b.do_something()
