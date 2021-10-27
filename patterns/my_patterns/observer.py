# coding: utf-8
"""Паттерн наблюдатель."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class Observer(ABC):
    """Интерфейс наблюдателя."""

    @abstractmethod
    def update(self: Observer, data: Dict) -> None:
        """Метод для получения данных от издателя."""
        ...


class ConcreteObserver(Observer):
    """Реализация наблюдателя."""

    def update(self: Observer, data: Dict) -> None:
        """Получает данные от издателя."""
        print(data)


class Subject(ABC):
    """Интерфейс издателя(владельца данных)."""

    @abstractmethod
    def registrate_observer(self: Subject, observer: Observer) -> None:
        """Регистрируем наблюдателей."""
        ...

    @abstractmethod
    def remove_registrate_observer(self: Subject, observer: Observer) -> None:
        """Удаление регистрации наблюдателя."""
        ...

    @abstractmethod
    def notify(self: Subject) -> None:
        """Оповещает наблюдателей от изменении данных."""
        ...


class ConcreteSubject(Subject):
    """Реализация издателя."""

    _observers: List[Observer] = []
    _data: Dict[str, int] = {"a": 1, "b": 2}

    def registrate_observer(self: ConcreteSubject, observer: Observer) -> None:
        """Регистрируем наблюдателей."""
        self._observers.append(observer)

    def remove_registrate_observer(self: ConcreteSubject, observer: Observer) -> None:
        """Удаление регистрации наблюдателя."""
        self._data.remove(observer)

    def notify(self: ConcreteSubject) -> None:
        """Оповещает наблюдателей от изменении данных."""
        for observer_i in self._observers:
            observer_i.update(self._data)


if __name__ == "__main__":
    subject = ConcreteSubject()
    observer_1 = ConcreteObserver()
    observer_2 = ConcreteObserver()
    subject.registrate_observer(observer_1)
    subject.registrate_observer(observer_2)
    subject.notify()
