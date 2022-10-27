# coding: utf-8

# 7.8. Заставляем вызываемый объект с N аргументами работать так же, как вызываемый объект с 
# меньшим количеством аргументов

from functools import partial
from inspect import signature


def spam(a, b, c, d):
    print(a, b, c, d)


print(f"signature of spam {signature(spam)}")


s1 = partial(spam, 1)  # a = 1
print(f"signature of s1 {signature(s1)}")
s1(2, 3, 4)
s1(4, 5, 6)

s2 = partial(spam, d=42)  # d = 42
print(f"signature of s2 {signature(s2)}")
s2(1, 2, 3)
s2(4, 5, 5)

s3 = partial(spam, 1, 2, d=42)  # a = 1, b = 2, d = 42
print(f"signature of s3 {signature(s3)}")
s3(3)
s3(4)
#  s3(2, 3, 4) Error

##############################################

points = [(1, 2), (3, 4), (5, 6), (7, 8)]
import math


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


"""
А теперь предположим, что вы хотите отсортировать все точки по их расстоя­
нию до какой-то другой точки. Метод списков sort() принимает аргумент key,
который может быть использован для настройки поиска, но он работает только
с функциями, которые принимают один аргумент (то есть distance() не подходит).
Вот как вы можете использовать partial(), чтобы решить данную проблему:
"""
pt = (4, 3)
points.sort(key=partial(distance, pt))
print(points)

# или
points.sort(key=lambda p: distance(pt, p))

# Работает и для классов
"""
class EchoHandler(StreamRequestHandler):
    # ack – это добавленный обязательный именованный аргумент.
    # *args, **kwargs – это любые обычные предоставленные параметры
    # (которые переданы)

    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)

serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))

"""
