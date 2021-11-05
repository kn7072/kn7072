# coding: utf-8
"""Паттерт прототип."""
from __future__ import annotations

from copy import copy, deepcopy


class Prototype:
    """Класс позволяющий клонировать свои экземпляры."""

    def __init__(self: Prototype, state: dict) -> None:
        """Инициализирует экземпляр."""
        self._state = state

    @property
    def state(self: Prototype) -> dict:
        """Возвращает состояние."""
        return self._state

    def __copy__(self: Prototype) -> Prototype:
        """Создает поверхностную копию.

        Метод вызывается при вызове метода copy, позволяет определять, что нужно копировать.
        """
        clone_object = Prototype(self._state)
        clone_object.__dict__ = copy(self.__dict__)
        return clone_object

    def __deepcopy__(self: Prototype, memo: dict = None) -> Prototype:
        """Создает полную копию экземпляра.

        Метод вызывается при вызове метода deepcopy, позволяет определять, что нужно копировать.
        """
        clone_object = Prototype(self._state)
        clone_object.__dict__ = deepcopy(self.__dict__, memo=memo)
        return clone_object


if __name__ == "__main__":
    state = {"a": 1, "b": 2}
    first_object = Prototype(state)

    copy_clone = copy(first_object)
    deepcopy_clone = deepcopy(first_object)

    state["a"] = "7"
    state["c"] = "10"
    print(f"first_object.state   {first_object.state}")
    print(f"copy_clone.state     {copy_clone.state}")
    print(f"deepcopy_clone.state {deepcopy_clone.state}")
