# -*- coding:utf-8 -*-


class A:
    x = 5


class B:
    c = A()

    def __init__(self):
        self.c.x = 10

b = B()
print(b.c.x)
print(B.c.x)

t = B()
print(t.c.x)