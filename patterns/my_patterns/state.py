# coding: utf-8
"""Паттерн состояние."""
from __future__ import annotations
import random

from abc import ABC, abstractmethod


class State(ABC):
    """Интерфейс состояния."""

    def __init__(self: State, context: Context) -> None:
        """Инициализация состояния."""
        self._context = context

    @abstractmethod
    def insert_quarter() -> None:
        """Вставить монету в автомат."""
        ...

    @abstractmethod
    def eject_quarter() -> None:
        """Вернуть монету."""
        ...

    @abstractmethod
    def turn_crank() -> None:
        """Повернуть ручку автомата."""
        ...

    @abstractmethod
    def dispense() -> None:
        """Выдать шарик."""
        ...


class NoQuarterState(State):
    """В автомате нет монетки."""

    def insert_quarter(self: NoQuarterState) -> None:
        """Вставить монету в автомат."""
        print("Монета в автомате - пока все ок.")
        self._context.set_state(self._context.get_has_quarter_state())

    def eject_quarter(self: NoQuarterState) -> None:
        """Вернуть монету."""
        print("Чтобы вернуть монету - ее сначала нужно вставить в автомат.")

    def turn_crank(self: NoQuarterState) -> None:
        """Повернуть ручку автомата."""
        print("Вставте пожалуйста монету.")

    def dispense(self: NoQuarterState) -> None:
        """Выдать шарик."""
        print("-")


class HasQuarterState(State):
    """В автомат бросили монету."""

    def insert_quarter(self: NoQuarterState) -> None:
        """Вставить монету в автомат."""
        print("Вы уже втавили монету - можете повернуть рычаг и купить шарик и вернуть монету.")

    def eject_quarter(self: NoQuarterState) -> None:
        """Вернуть монету."""
        print("Возьмите Вашу монету.")
        self._context.set_state(self._context.get_no_quarter_state())

    def turn_crank(self: NoQuarterState) -> None:
        """Повернуть ручку автомата."""
        print("Спасибо что приорели шарик.")
        if random.randint(0, 10) == 7:
            self._context.set_state(self._context.get_winner_state())
        else:
            self._context.set_state(self._context.get_sold_state())

    def dispense(self: NoQuarterState) -> None:
        """Выдать шарик."""
        print("-")


class SoldState(State):
    """Сделка совершена - шарик считается проданным."""

    def insert_quarter(self: NoQuarterState) -> None:
        """Вставить монету в автомат."""
        print("Вы уже приобрели шарик - возьмите его. Затем можете вновь вставить монету.")

    def eject_quarter(self: NoQuarterState) -> None:
        """Вернуть монету."""
        print("Извените - сделка уже совершена.")

    def turn_crank(self: NoQuarterState) -> None:
        """Повернуть ручку автомата."""
        print("Извените - сделка уже совершена.")

    def dispense(self: NoQuarterState) -> None:
        """Выдать шарик."""
        self._context._count_ball -= 1
        if self._context._count_ball == 0:
            self._context.set_state(self._context.get_sold_out_state())
        else:
            self._context.set_state(self._context.get_no_quarter_state())
        print("Заберите шарик.")


class SoldOutState(State):
    """В автомате нет шариков."""

    def insert_quarter(self: NoQuarterState) -> None:
        """Вставить монету в автомат."""
        print("Шариков нет.")

    def eject_quarter(self: NoQuarterState) -> None:
        """Вернуть монету."""
        print("Шариков нет.")

    def turn_crank(self: NoQuarterState) -> None:
        """Повернуть ручку автомата."""
        print("Шариков нет.")

    def dispense(self: NoQuarterState) -> None:
        """Выдать шарик."""
        print("")


class WinnerState(State):
    """За одну монету - два шарика."""

    def insert_quarter(self: NoQuarterState) -> None:
        """Вставить монету в автомат."""
        print("Вы уже приобрели шарик - возьмите его. Затем можете вновь вставить монету.")

    def eject_quarter(self: NoQuarterState) -> None:
        """Вернуть монету."""
        print("Извените - сделка уже совершена.")

    def turn_crank(self: NoQuarterState) -> None:
        """Повернуть ручку автомата."""
        print("Извените - сделка уже совершена.")

    def dispense(self: NoQuarterState) -> None:
        """Выдать два шарика."""
        if self._context._count_ball > 2:
            self._context._count_ball -= 2
        else:
            self._context._count_ball -= 1

        if self._context._count_ball == 0:
            self._context.set_state(self._context.get_sold_out_state())
        else:
            self._context.set_state(self._context.get_no_quarter_state())
        print("Заберите шарик.")


class Context:
    """Автомат с шариками."""

    def __init__(self: Context, count_ball: int) -> None:
        """Инициализация автомата."""
        self._count_ball = count_ball
        self._sold_out_state = SoldOutState(self)
        self._has_quarter_state = HasQuarterState(self)
        self._no_quarter_state = NoQuarterState(self)
        self._sold_state = SoldState(self)
        self._winner_state = WinnerState(self)
        if count_ball > 0:
            self._state = self._no_quarter_state
        else:
            self._state = self._sold_out_state

    def insert_quarter(self: Context) -> None:
        """Вставляет монету в автомат."""
        self._state.insert_quarter()

    def eject_quarter(self: Context) -> None:
        """Запрос на возврат монета."""
        self._state.eject_quarter()

    def turn_crank(self: Context) -> None:
        """Повернуть рычаг - чтобы сделка состоялась."""
        self._state.turn_crank()
        self._state.dispense()

    def set_state(self: Context, state: State) -> None:
        """Изменяет состояние автомата."""
        self._state = state

    def get_no_quarter_state(self: Context) -> NoQuarterState:
        """Геттер для получения состояния NoQuarterState."""
        return self._no_quarter_state

    def get_has_quarter_state(self: Context) -> HasQuarterState:
        """Геттер для получения состояния HasQuarterState."""
        return self._has_quarter_state

    def get_sold_out_state(self: Context) -> SoldOutState:
        """Геттер для получения состояния SoldOutState."""
        return self._sold_out_state

    def get_sold_state(self: Context) -> SoldState:
        """Геттер для получения состояния SoldState."""
        return self._sold_state

    def get_winner_state(self: Context) -> WinnerState:
        """Геттер для получения состояния WinnerState."""
        return self._winner_state


if __name__ == "__main__":
    context = Context(count_ball=10)
    context.insert_quarter()  # вставили монету
    context.eject_quarter()  # верните монету

    context.insert_quarter()
    context.turn_crank()  # покупаю шарик
