# -*- coding:utf-8 -*-

def wrapper(fun, name):
    def x():
        return fun
    x.__name__ = name
    return x

class A:
    def method(self):
        print(3)

dict_ = A.__dict__['method']
for i in range(3):
    setattr(A, 'test_add_%s' % i, wrapper(dict_, name='test_add_%s' % i))
print("test")
a = A()


print()
