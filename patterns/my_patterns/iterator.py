# coding:utf-8
"""Паттерн итератор."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class Iterator(ABC):
    """Интерфейс итератора."""

    @abstractmethod
    def next(self: Iterator) -> Any:
        """Возвращает следующий элемент коллекции."""
        ...

    @abstractmethod
    def has_next(self: Iterator) -> bool:
        """Проверяет, существование следующего элемента коллекции."""
        ...


class ConcreteIterator(Iterator):
    """Реализация итератора."""

    def __init__(self: Iterator, collection: List) -> None:
        """Инициализирует экземпляр класса."""
        super().__init__()
        self._collection = collection
        self._index = 0

    def next(self: Iterator) -> str:
        """Метод для получения следующего элемента коллекции."""
        current_element = self._collection[self._index]
        self._index += 1
        return current_element

    def has_next(self: Iterator) -> bool:
        """Проверяет, существование следующего элемента коллекции."""
        return False if self._index >= len(self._collection) else True


test_collection = ["1", "2", "3"]
iterator = ConcreteIterator(test_collection)
while iterator.has_next():
    print(iterator.next())
