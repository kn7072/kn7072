# coding: utf-8
"""Паттерт посредник."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Mediator(ABC):
    """Интерфейс посредника."""

    @abstractmethod
    def notify(self: Mediator, sender: BaseComponent, event: str) -> None:
        """Метод для взаимодейстия компонентов."""
        ...


class ConcreteMediator(Mediator):
    """Реализация посредника."""

    def __init__(self: ConcreteMediator, component1: Component1, component2: Component2) -> None:
        """Инициализирует объект."""
        self._component1 = component1
        self._component1.mediator = self
        self._component2 = component2
        self._component2.mediator = self

    def notify(self: ConcreteMediator, sender: BaseComponent, event: str) -> None:
        """Что-то делает."""
        if event == "A":
            print("Mediator reacts on A and triggers following operations:")
            self._component2.do_c()
        elif event == "D":
            print("Mediator reacts on D and triggers following operations:")
            self._component1.do_b()
            self._component2.do_c()


class BaseComponent:
    """Базовый компонент.

    Обеспечивает базовую функциональность хранения экземпляров.
    """

    def __init__(self: BaseComponent, mediator: Mediator) -> None:
        """Инициализирует объект."""
        self._mediator = mediator

    @property
    def mediator(self: BaseComponent) -> Mediator:
        """Возвращает медиатор."""
        return self._mediator

    @mediator.setter
    def mediator(self: BaseComponent, mediator: Mediator) -> None:
        """Устанавливает медиатор."""
        self._mediator = mediator


if __name__ == "__main__":
    pass
