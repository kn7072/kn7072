# coding: utf-8
"""Простой север - Корутины и yield from - Лекция 6 https://www.youtube.com/watch?v=5SyA3lsO_hQ&list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8&index=6 ."""
from __future__ import annotations

import types
from typing import Any, Dict, Generator, List, Optional


def coroutine(fun: types.FunctionType) -> types.FunctionType:
    """Принимает функцию генератор, возвращает функцию обертку."""
    def inner_function(*args: Optional[List[Any]], **kargs: Dict) -> Generator:
        """Возвращает генератор."""
        generator = fun(*args, **kargs)
        generator.send(None)
        return generator
    return inner_function


class MyExeption(Exception):
    """Пользовательское исключение."""

    pass


@coroutine
def subgen() -> None:
    """Подгенеретор."""
    while True:
        try:
            message = yield
        except StopIteration:
            break
        except MyExeption:
            print("subgen MyExeption")
        else:
            print(".....", message)


@coroutine
def delegator(generator: Generator) -> str:
    """Делегирует работу подгенератору."""
    while True:
        try:
            data = yield
            generator.send(data)
        except StopIteration:
            break
        except MyExeption as e:
            print("delegator MyExeption")
            generator.throw(e)


def subgen_for_yield_from() -> str:
    """Для yield from."""
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print(".....", message)
    # результат будет помещен в переменную result, из result = yield from generator
    return "Returned from subgen()"


@coroutine
def delegator_for_yield_from(generator: Generator) -> str:
    """Делегирует работу подгенератору."""
    result = yield from generator
    print(result)


if __name__ == "__main__":
    sub_generator = subgen()
    generator = delegator(sub_generator)
    generator.send("Ok")
    generator.throw(MyExeption)

    sub_generator_2 = subgen_for_yield_from()
    generator_2 = delegator_for_yield_from(sub_generator_2)
    generator_2.send("HELLO")
    generator_2.throw(StopIteration)
