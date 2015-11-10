def ny_fun(self):
    def __get__(*args):
        print()
    def __set__(*args):
        print()
    print('150')

def yyy(*args):
    print()

def class_fun(self):
    print('xxxx')

def wraper(x):
    x.__self__
    print()
class Stack():
    def __init__(self):    # Инициализация стека
        self.stack = [ ]
    y = ny_fun
    def push(self,object):
        self.stack.append(object)
    def pop(self):
        return self.stack.pop()
    def length(self):
        return len(self.stack)
    def __get__(self):
        pass

f = Stack()
setattr(Stack, 'FUNC', class_fun)
f.__dict__['x'] = ny_fun  #
mro = type(f.FUNC).__mro__
setattr(f.x.__class__,'__get__', yyy)
#f.x.__class__ = Stack# mro[0]
f.x()
f.__dict__['__self__'] = f
f.x.__get__(f)()
# f.x error
###################################################
class D:
    def f(self, x):
        return x
d = D()
k = D()
print(d.f)
wraper(d.f)
print(D.f)
print(D.__dict__['f'])
print()