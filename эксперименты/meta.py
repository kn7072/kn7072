class Meta(type):
    def __new__(meta, classname, supers, classdict):
        # Run by inherited type.__call__
        return type.__new__(meta, classname, supers, classdict)

class MetaOne(type):
    def __new__(meta, classname, supers, classdict):
        print('In MetaOne.new:', classname, supers, classdict)
        return type.__new__(meta, classname, supers, classdict)

class Eggs:
    def __init__(self):
       setattr(self, 'c', 1)
    pass

print('making class')
class Spam(Eggs, metaclass=MetaOne):      # Inherits from Eggs, instance of Meta
    data = 1                              # Class data attribute
    def meth(self, arg):                  # Class method attribute
        pass

print('making instance')
class MetaTest(type):
    def __new__(cls, name, bases, dict):
        klass = super(MetaTest, cls).__new__(cls,name, bases, dict)  #
        print ("__new__(%r, %r, %r) -> %r" % (name, bases, dict, klass))
        print("__new__({0},{1},{2},{3})".format(cls, name, bases, dict))
        return klass
    def __init__(cls, name, bases, dict):
        print ("__init__(%r, %r, %r)" % (name, bases, dict))
        print("__init__({0},{1},{2},{3})".format(cls, name, bases, dict))
        type.__init__(cls, name, bases, dict)
    def __call__(cls, *args, **kwargs):
        obj = super(MetaTest, cls).__call__(*args, **kwargs)
        print ("__call__(%r, %r) -> %r" % (args, kwargs, obj))
        return obj
class Test(metaclass=MetaTest):
    def __init__(self):
        self.f = 9
    def __call__(cls, *args, **kwargs):
        print("ss")
    pass
class Prop(Test):
    def __init__(self):
        print("d")
    def __call__(cls, *args, **kwargs):
        print("Prop")

class AutoSuper(type):
    def __init__(cls, name, bases, dict):
        super(AutoSuper, cls).__init__(name, bases, dict)
        setattr(cls, "_%s__super" % name, super(cls))

class A(metaclass=AutoSuper):
    def method(self):
         return "A"
class B(A):
     def method(self):
         return "B" + A.method(self)  # self.__super

class M_f(type): pass
class M_h(type): pass
class T(metaclass = M_f):pass
class G(metaclass = M_h):pass
M_fM_h = type("M_AM_B", (M_f,M_h), {})
class C(T,G, metaclass = M_fM_h): pass

if __name__=='__main__':
    prop = Prop()
    q = B()
    s = q.method()
    a = A()
    s = q.method()


    e = Eggs().__dict__
    test = Test()
    t = Eggs
    r = t()

    y = Spam
    x = Spam()
    print('data:', x.data)