# coding: utf-8
"""Паттерн легковес."""
from __future__ import annotations

from weakref import WeakValueDictionary


class FlyweightColor:
    """Хранит общую часть состояния(внешнее состояние)."""

    def __init__(self: FlyweightColor, color_name: str) -> None:
        """Инициализирует экземпляр."""
        self.color_name = color_name

    def __str___(self: FlyweightColor) -> str:
        """Возвращает строковое представление объекта."""
        return self.color_name


class FlyweightFactory:
    """Фабрика легковесов."""

    __slots__ = ()
    _colors = WeakValueDictionary()

    @classmethod
    def get_color(cls: FlyweightFactory, color_name: str) -> FlyweightColor:
        """Возвращает объект цвета(внешнего состояния)."""
        object_color = cls._colors.get(color_name)
        if object_color is None:
            object_color = FlyweightColor(color_name)
            cls._colors[color_name] = object_color
        return object_color


class PlaceMark:
    """Объект обладающий внутренним и внешнем состоянием(внешнее состояние храним отдельн)."""

    def __init__(self: PlaceMark, latitude: float, longitude: float, color_name: str) -> None:
        """Инициализирует экземпляр."""
        # цвет - это внешнее состояние - такие состояния повторяются - храним их отдельно.
        self._latitude = latitude
        self._longtitude = longitude
        self._color = FlyweightFactory.get_color(color_name)

    def __str__(self: PlaceMark) -> str:
        """Строковое представление объекта."""
        return f"Координаты {self._latitude}/{self._longtitude}, цвет {self._color}.\n"


if __name__ == "__main__":
    mark_0 = PlaceMark(1.1, 2.2, "red")
    mark_1 = PlaceMark(3.3, 4.4, "red")
    mark_2 = PlaceMark(5.5, 6.6, "green")

    print(mark_0, mark_1, mark_2, end="\n")
