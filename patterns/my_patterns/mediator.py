# coding: utf-8
"""Паттерт посредник."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Mediator(ABC):
    """Интерфейс посредника."""

    @abstractmethod
    def notify(self: Mediator, event: str) -> None:
        """Метод для взаимодейстия компонентов."""
        ...


class ConcreteMediator(Mediator):
    """Реализация посредника."""

    def notify(self: ConcreteMediator, event: str) -> None:
        """Что-то делает."""
        ...

