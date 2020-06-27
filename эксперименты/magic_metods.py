# -*- coding: utf-8 -*-

class DataDesc:

    def __init__(self, x=0):
        self.x = x

    def __get__(self, obj, cls):
        print("Trying to access from {0} class {1}".format(obj, cls))

    def __set__(self, obj, val):
        print("Trying to set {0} for {1}".format(val, obj))

    def __delete__(self, obj):
        print("Trying to delete from {0}".format(obj))

    def method(self):
        print('method')


class DemoMagic:

    desc = DataDesc()
    def __init__(self, atr):
        self.atf = atr
        self.descripror_data = DataDesc()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        print(key)
    # def __dir__(self):
    #     print("dir")

demo = DemoMagic(100)
demo.atf = 50
demo.__setattr__('z', 10)
# переопределили setattr должно все сломаться - но не сломалось
demo.__setattr__ = lambda self: 44
# demo.__setattr__      demo.__dict__['__setattr__']
setattr(demo, 'x', 77)
setattr(DemoMagic, 'magic', 55)
demo.__dir__()
demo.descripror_data
demo.desc
#dir(demo)
print()