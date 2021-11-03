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
def test() -> int:
    """Функция генератор."""
    count_iter = 0
    while True:
        try:
            temp = yield count_iter
            print(f"print {temp}")
            count_iter += 1
        except StopIteration:
            print("StopIteration")
            break
        except MyExeption:
            print("MyExeption")
            break
    return count_iter


if __name__ == "__main__":
    generator = test()
    try:
        generator.throw(MyExeption)
    except StopIteration as e:
        # только так можно получить значение возвращаемое через return
        print(f"result {e.value}")
    print()
