# -*- coding: utf-8 -*-

def wrap(fun, a,b):
    def x(self):
        fun(self, a,b)
        #print(a,b)
    return x
# z = wrap(3,5)
# z()
# l = wrap(7,9)
# l()
# z()
def decor(f):
    def wrap_metod(self, *args):#
        print('sssss')
        f(self, 3,5)
    return wrap_metod

def add_method(cls, name, fun, arg):
    setattr(cls, name, wrap(fun, *arg))

class S:
    @decor
    def metod(self, x, y):
        print(x,y)

s = S()
add_method(S, "method_1", S.metod, (2,4))
add_method(S, "method_2", S.metod, (5,6))
s.metod
