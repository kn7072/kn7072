class MetaTest(type):
    def __new__(cls, name, bases, dict):
        x = super(MetaTest, cls)
        klass = super(MetaTest, cls).__new__(cls, name, bases, dict)  #
        #print ("__new__(%r, %r, %r) -> %r" % (name, bases, dict, klass))
        print("__new__({0},{1},{2},{3})".format(cls, name, bases, dict))
        return klass
    def __init__(cls, name, bases, dict):
        #print ("__init__(%r, %r, %r)" % (name, bases, dict))
        print("__init__({0},{1},{2},{3})".format(cls, name, bases, dict))
        #type.__init__(cls, name, bases, dict)
        x = super(MetaTest, cls)
        super(MetaTest, cls).__init__(name, bases, dict)
        setattr(cls, 'fff', 'sssssssss')
        pass
    def __call__(cls, *args, **kwargs):
        obj = super(MetaTest, cls).__call__(*args, **kwargs)
        print ("__call__(%r, %r) -> %r" % (args, kwargs, obj))
        return obj
class Test(metaclass=MetaTest):
    def __init__(self):
        self.f = 9
    def __call__(cls, *args, **kwargs):
        print("ss")

z = Test()
print(3)