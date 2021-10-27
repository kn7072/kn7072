# coding:utf-8
"""Паттерн стратегия."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Context():
    """Класс использующий стратегию."""

    def __init__(self: Context, straregy: Strategy) -> None:
        """Инициализирует экземпляр класса."""
        super().__init__()
        self._strategy = straregy

    @property
    def strategy(self: Context) -> Strategy:
        """Свойство для получения текущей стратегии."""
        return self._strategy

    @strategy.setter
    def strategy(self: Context, strategy: Strategy) -> None:
        """Сеттер для смены стратегии."""
        self._strategy = strategy

    def do_some_useful(self: Context) -> None:
        """Метод использующий объект стратегии."""
        self._strategy.do_algorithm()


class Strategy(ABC):
    """Интерфейс стратегии."""

    @abstractmethod
    def do_algorithm(self: Strategy) -> None:
        """Абстрактный метод."""
        ...


class ConcreteStrategy1(Strategy):
    """Реализация стратегии."""

    def do_algorithm(self: ConcreteStrategy1) -> str:
        """Метод который что-то делает."""
        const = "ConcreteStrategy1"
        print(const)
        return const


class ConcreteStrategy2(Strategy):
    """Реализация стратегии."""

    def do_algorithm(self: ConcreteStrategy2) -> str:
        """Метод который что-то делает."""
        const = "ConcreteStrategy2"
        print(const)
        return const


if __name__ == "__main__":
    context = Context(ConcreteStrategy1())
    context.strategy.do_algorithm()

    context.strategy = ConcreteStrategy2()
    context.strategy.do_algorithm()
