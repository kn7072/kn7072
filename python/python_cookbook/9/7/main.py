# coding: utf-8

"""
9.7. Принудительная проверка типов в функции с использованием декоратора

Задача
Вы хотите иметь возможность включить принудительную проверку типов аргу-
ментов функции.

"""

from functools import wraps
from inspect import signature


def typeassert(*ty_args, **ty_kwargs):

    def decorate(func):
        # Если мы в оптимизированном режиме, отключаем проверку типов
        if not __debug__:
            return func

        # Отображаем имена аргументов функции на предоставленные типы
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Принудительно проверяем типы предоставленных аргументов ассертами
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)

        return wrapper

    return decorate


@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)

"""
Во-первых, одна из особенностей декораторов в том, что они применяются
только один раз, во время определения функции. В некоторых случаях вы можете
захотеть отключить функциональность, добавленную декоратором. Чтобы сде-
лать это, просто заставьте ваш декоратор вернуть необернутую функцию. В ре-
шении приведенный ниже фрагмент кода возвращает неизмененную функцию,
если значение глобальной переменной __debug__ установлено на False (как и в том
случае, когда интерпретатор Python запускается в оптимизированном режиме
с параметрами -O или -OO)
""""

spam(1, 2, 3)
spam(1, 'hello', 3)
spam(1, 'hello', 'world')
