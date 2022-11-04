# coding: utf-8

"""
17.2.4.1. Необработанные исключения
Структура многих приложений включает основной цикл, который обертывает
выполняемый код глобальным обработчиком исключений, перехватывающим те
ошибки, что не были обработаны на более низком уровне. Можно получить тот
же результат, установив в качестве перехватчика sys .excepthook функцию, получающую
три аргумента (тип ошибки, значение ошибки и объект трассировки),
и поручив ей обработкуошибок, оставшихся необработанными.

Поскольку строка, в которой возникло исключение, не находится в блоке
try:except, следующий за ней вызов функции print() не выполняется, хотя
и установлен перехватчик исключений.
"""

import sys
import traceback


def my_excepthook(type, value, traceback):
    print('Unhandled error:', type, value)

def show_exception_and_exit(exc_type, exc_value, tb):
    print('show_exception_and_exit')
    traceback.print_exception(exc_type, exc_value, tb)
    sys.exit(-1)

# sys.excepthook = my_excepthook
sys.excepthook = show_exception_and_exit

print('Before exception')
raise RuntimeError('This is the error message')
print('After exception')