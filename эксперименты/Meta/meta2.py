import traceback


class Ameta(type):
    def foo(cls):
        print ('Ameta.foo')

class X ():
    s = 4
    def __init__(self):
        self.f = 's'
    def g(self):
        print (self)

class A(metaclass=Ameta):
    #__metaclass__ = Ameta
    x = 22
    pass
class Meta(type):
    # cls = type.__dict__['__new__'](Meta, 'A', (object,), {})
    # type.__dict__['__init__'](cls, 'A', (object,), {})
    pass

def my_method(self):
    print("f")

class Meta2(type):

     x = 22
     def __call__(cls, *args, **kwargs):
         obj = super(Meta2, cls).__call__(*args, **kwargs)
         print("__call__(%r, %r) -> %r" % (args, kwargs, obj))
         return obj
     def __new__(mcls, name, bases, attrs):
         print ('creating new class', name)
         class_ = super(Meta2, mcls).__new__(mcls, name, bases, attrs)
         return class_
     def __init__(cls, name, bases, attrs):
         setattr(cls, 'my', my_method)
         print ('initing new class', name)


class B(metaclass=Meta2):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        self.b = 4
    def __call__(self, *args, **kwargs):
        return self.b
    def method(self):
         q = traceback.extract_stack()
         print("method")
         return "A"

class E ():
    pass
if __name__ == '__main__':
    b = B()
    b.method()
    w = b()
    q = type.__call__(E)
    q2 = type.__call__(E)
    q3 = type.__call__(E)
    d = dict(X.__dict__)
    d1 = X()
    d2 = d1.__dict__
    d1.__dict__['ss']=1
    cls = type.__dict__['__new__'](Meta, 'W', (object,), d)
    type.__dict__['__init__'](cls, 'W', (object,), d2)
    y= Meta('A', (object,), {})
    X.s
    #Ameta.foo()
    #X.g()
    s = A
    s.foo()