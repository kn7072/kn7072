# coding: utf-8

import sys


"""
17.2.1.6. Перехват вывода
Функция sys.displayhook() вызывается интерактивным интерпретатором
всякий раз, когда пользователь вводит выражение. Результат вычисления выражения
передастся этой функции в качестве единственного аргумента.

Значение по умолчанию (сохраненное в sys.__displayhook__ ) выводится
в качестве результата в стандартный поток stdout и сохраняется в переменной _,
на которую впоследствии можно легко ссылаться.

>>> import sys_displayhook
>>> 1 + 2
>>> 3
"""

class ExpressionCounter:
    def __init__(self) :
        self.count = 0
        self.previous_value = self
        
    def __call__(self, value):
        print()
        print(' Previous:', self.previous_value)
        print(' New :', value)
        print()
        if value != self.previous_value:
            self.count += 1
            sys.psl = '({:3d})> '.format(self.count)
        self.previous_value = value
        sys.__displayhook__(value)

print('installing')
sys.displayhook = ExpressionCounter()