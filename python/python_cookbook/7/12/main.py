# coding: utf-8

# 7.12. Доступ к переменным, определенным внутри замыкания

"""
Задача
Вы хотите добавить в замыкание функции, которые позволят получать доступ
и изменять внутренние переменные.

"""

import sys


def sample():
    n = 0

    # Функция-замыкание
    def func():
        print('n=', n)

    # Методы доступа к n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Прикрепление в качестве атрибутов функции
    func.get_n = get_n
    func.set_n = set_n

    return func


f = sample()
f()

f.set_n(10)
f()

f.get_n()

"""
Небольшое дополнение к этому рецепту позволит замыканиям эмулировать
экземпляры класса. Все, что вам нужно, – это скопировать внутренние функции
в словарь экземпляра и возвратить его. Например:

"""


class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

            locals_0 = sys._getframe(0).f_locals
            locals_2 = sys._getframe(2).f_locals
            # Обновить словарь экземпляра вызываемыми объектами
            self.__dict__.update((key, value) for key, value in locals.items() if callable(value))

    # перегружаем специальные методы
    def __len__(self):
        return self.__dict__['__len__']()


# Пример использования
def Stack():
    items = []
    
    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()


def new_method_a(a):
    print(a)


def new_method_b(self, b):
    print(b)


def new_method_с(self, с):
    print(с)

s = Stack()
print(s)

# ОТСТУПЛЕНИЕ ОТ ПРИМЕРА ИЗ КНИГИ - ЭКСПЕРИМЕНТЫ
print(s.__dict__)
s.__dict__.update({"new_method_a": new_method_a})
print(s.__dict__)
s.new_method_a(7)  # вызывается как простая функция

s.__dict__.update({"new_method_b": new_method_b})
print(s.__dict__)
# s.new_method_b(7)  # TypeError

# способ связать функцию и экземпляр
from functools import partial
s.__dict__.update({"new_method_b": partial(new_method_b, s)})
s.new_method_b(7)

new_method_с.__get__(s, Stack)(10)
# ЭКСПЕРИМЕНТ ЗАКОНЧЕН

s.push(10)
s.push(20)
s.push('Hello')
len(s)

s.pop()  # 'Hello'
s.pop()  # 20
s.pop()  # 10

"""
Интересно, что этот код работает немного быстрее аналога, использующего
обычное определение класса. Например, вы можете проверить производитель-
ность по сравнению с таким классом:


"""


class Stack2:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)


"""
Как показано выше, версия на базе замыкания работает на 8 % быстрее. По
большей части выигрыш возникает за счет прямого доступа к переменным эк-
земпляра. Замыкания быстрее, потому что не используют дополнительную пере-
менную self.

"""