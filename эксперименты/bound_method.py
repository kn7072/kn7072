# -*- encoding: utf-8 -*-

class A():

    def x(self, y):
        print(self, y)

a = A()
m_unbound = A.x
m_unbound_dict = A.__dict__['x']
m_bound = a.x
a.__class__.x.__get__(a)(5)
print()