# coding: utf-8

"""
9.8. Определение декораторов как части класса

Задача
Вы хотите определить декоратор внутри определения класса и применить его
к другим функциям или методам.

"""

from functools import wraps


class A:

    # Декоратор как метод экземпляра
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)
        return wrapper

    # Декоратор как метод класса
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)
        return wrapper


# Как метод экземпляра
a = A()

@a.decorator1
def spam():
    pass

# Как метод класса
@A.decorator2
def grok():
    pass


"""
Обсуждение
Определение декораторов в классе на первый вгляд может показаться странным,
но примеры такого подхода вы встретите даже в стандартной библиотеке. В част-
ности, встроенный декоратор @property на самом деле является классом с мето-
дами getter(), setter() и deleter(), каждый из которых действует как декоратор. На-
пример:

"""


class Person:
    # Создание экземпляра свойства
    first_name = property()

    # Применение методов декоратора
    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
