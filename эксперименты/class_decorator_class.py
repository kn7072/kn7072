# -*- coding:utf-8 -*-


class Decorator:

    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, item):
        return self.cls.__dict__[item]

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)


@Decorator
def fun(a, b):
    print(a+b)


@Decorator  # x = Decorator(x)
class Victim:

    def __init__(self, a):
        self.a = a
        print(a)

    def method_victim(self):
        print('hallo world')

f = fun(2, 3)
v = Victim(1)
v.method_victim()
print()