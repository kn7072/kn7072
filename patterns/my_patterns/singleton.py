# coding: utf-8
"""Паттерн одиночка."""
from __future__ import annotations

from typing import Any, Optional


class Singleton(type):
    """Интерфейс одиночки."""

    _instance: Optional[Singleton] = None

    def __call__(cls: Singleton, *args: Any, **kwds: Any) -> Singleton:
        """Вызывается при создании экземпляра."""
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwds)
        return cls._instance


class MyClass(metaclass=Singleton):
    """Одиночка."""

    def __init__(self: MyClass, data: str) -> None:
        """Инициализирует экземпляр класса."""
        self.data = data


if __name__ == "__main__":
    singleton_1 = MyClass("test_text")
    print(singleton_1.data)

    singleton_2 = MyClass("test_text_1")
    print(singleton_1.data)
    print(singleton_2.data)
    assert id(singleton_1) == id(singleton_2), "Должны быть равны"
