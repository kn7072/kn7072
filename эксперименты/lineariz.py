#from atf import *
import inspect, sys, pdb
import sys
class Music(object): pass
class Rock(Music): pass
class Gothic(Music): pass
class Metal(Rock): pass
class GothicRock(Rock, Gothic): pass
class GothicMetal(Metal, Gothic): pass
class The69Eyes(GothicRock, GothicMetal): pass
a = 'Hello world'
b = a
print(sys.getrefcount(a))
x = The69Eyes()
def s(i,j):
    i(j)

class E:

    locals()['hallo']=lambda self, x:'world'
    def __init__(self):
        pass
    def x(self, x):
        print(x)
        #pdb.set_trace()
        self.e=3
        locals()['hallo']=lambda self, t:'world'
        print(4)

    def y(self):
        print(self.e)
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)
a = E()
a.x(3)
d= a
c = a
print(sys.getrefcount(a)-1)  # Возвращает значение счетчика ссылок на объект object.
setattr(E,'S', 3)
e =E()
s(a.x, 4)
a.x(2)
a.y()
pass
if __name__=="__main__":
    s = E()