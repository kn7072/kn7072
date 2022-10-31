# coding: utf-8

"""
9.13. Использование метакласса для управления созданием экземпляров

Задача
Вы хотите изменить процесс создания экземпляров с целью реализовать синглтон,
кеширование или другие похожие возможности.
"""

import weakref

class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# Пример
class Spam(metaclass=Cached):
    def __init__(self, name, sub_name):
        print('Creating Spam({!r}) {}'.format(name, sub_name))
        self.name = name


a = Spam('Guido', "a")
b = Spam('Diana', 'b')
c = Spam('Guido', "a")  # Закеширован
print(a is b)
False
print(a is c)  # Возвращается закешированное