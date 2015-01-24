# -*- encoding:utf-8 -*-
class t:
    tt=44
class x:
    def __init__(self):
        for key in self.__class__.__dict__.keys():
            if isinstance(self.__class__.__dict__[key], t):
                self.__class__.__dict__[key].driver = 100
    a=t()

class c(x):
    def __init__(self):
        super().__init__()
    b=t()

class d(c):
    def __init__(self):
        super().__init__()
        self.t = 5
    k = t()

r = d()
print()
