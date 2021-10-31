# coding: utf-8
"""Паттерн снимок."""
from __future__ import annotations

from copy import deepcopy
import random
from typing import List


class Momento:
    """Объект для хранения состояния объекта Originator."""

    def __init__(self: Momento, state: dict) -> None:
        """Инициализирует объект."""
        self._state = state

    def get_state(self: Momento) -> dict:
        """Возвращает состояние."""
        return self._state


class Caretaker:
    """Хранитель состояний."""

    def __init__(self: Caretaker, originator: Originator) -> None:
        """Инициализирует объект."""
        self._originator = originator
        self._momentos: List[Momento] = []

    def backup(self: Caretaker) -> None:
        """Создает снимок состояния."""
        self._momentos.append(self._originator.save())

    def undo(self: Caretaker) -> None:
        """Перейти в предыдущее состояние."""
        if not len(self._momentos):
            return
        momento = self._momentos.pop()
        print(f"Переключаемся в состояние {momento.get_state()}.")
        self._originator.restore(momento)


class Originator:
    """Класс, состояние объектов которого будем хранить."""

    def __init__(self: Originator) -> None:
        """Инициализирует объект."""
        self._state = {"a": 1, "b": 2}

    def save(self: Originator) -> None:
        """Сохраняет состояние объекта."""
        return Momento(deepcopy(self._state))

    def restore(self: Originator, momento_state: Momento) -> None:
        """Восстановить состояние."""
        self._state = momento_state.get_state()

    def do_something(self: Originator) -> None:
        """Что-то делает и изменяется состояние."""
        self._state["a"] = random.randint(1, 7)

    def print_state(self: Originator) -> None:
        """Разпечатать состояние - отладочная."""
        print(self._state)


if __name__ == "__main__":
    originator = Originator()
    caretaker = Caretaker(originator)
    caretaker.backup()
    originator.print_state()

    originator.do_something()
    caretaker.backup()
    originator.print_state()

    originator.do_something()
    originator.print_state()
    caretaker.undo()
    originator.print_state()
