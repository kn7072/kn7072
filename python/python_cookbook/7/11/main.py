# coding: utf-8

# 7.11. Встроенные функции обратного вызова

from functools import wraps
from queue import Queue


class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args


def apply_async(func, args, *, callback):
    # Вычисляем результат
    result = func(*args)
    # Вызываем функцию обратного вызова с результатом
    callback(result)


def inlined_async(func):

    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break

    return wrapper


def add(x, y):
    return x + y


@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')


test()