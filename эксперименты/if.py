#  -*- coding: utf-8 -*-
import inspect
import dict
a = 2
def mod():
    print(a)
dict.s(mod)
if True: pass
elif 5>3: pass
else:print('ddd')
class e :
    def __get__(self, instance, owner):
        print("get")
    def __set__(self, instance, value):
        print("set")
class dd:
    pass
class y(dd):

    des_data = e()
    def s(self):
        print('s')
    def x(self,a):
        print(a)
    def t (self, b):
        print(25)
    def see(self, name, value):
        print("set")
    x.__dict__['__get__'] = t
    x.__dict__['__set__'] = see
o = y()
o.__dict__['des_data']='dddddddd'
o.__dict__['s']='sdf'
o.x
o.x(4)
#y.__dict__['x'].__get__(y(), 2)
s = y.__dict__['x'].__get__(None, type(y)) # 25
y.t
y().x(5)
s = y()
y.x.__get__(s, 3)
y().x(5)