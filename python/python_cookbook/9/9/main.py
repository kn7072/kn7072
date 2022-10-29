# coding: utf-8

"""
9.9. Определение декораторов как классов

Задача
Вы хотите оборачивать функции декоратором, но результат должен быть вызы-
ваемым объектом. Вы хотите, чтобы ваш декоратор работал и внутри, и снаружи
определения класса.

"""

import types
from functools import wraps


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


class Spam:

    @Profiled
    def bar(self, x):
        print(self, x)


add(2, 3)
add(4, 5)
add.ncalls

s = Spam()
s.bar(1)
s.bar(2)
s.bar(3)
Spam.bar.ncalls
