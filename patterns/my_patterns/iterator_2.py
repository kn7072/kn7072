# coding: utf-8
"""Паттерн итератор."""
from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, List


class MyIterator(Iterator):
    """Класс итератор."""

    def __init__(self: MyIterator, collection: list) -> None:
        """Инициализирует экземпляр класса."""
        super().__init__()
        self._collection = collection
        self._index = 0

    def __next__(self: MyIterator) -> str:
        """Метод для получения следующего элемента коллекции."""
        try:
            value = self._collection[self._index]
            self._index += 1
        except IndexError:
            raise StopIteration

        return value


class CollectionMy(Iterable):
    """Класс коллекции."""

    def __init__(self: CollectionMy, collection: List[Any]) -> None:
        """Инициализирует экземпляр класса."""
        super().__init__()
        self._iterator = MyIterator(collection)

    def __iter__(self: CollectionMy) -> Iterator:
        """Возвращает объект итератор."""
        return self._iterator


test_collection = ["1", "2", "3"]
collection = CollectionMy(test_collection)
for i in collection:
    print(i)
