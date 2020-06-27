# coding: utf-8


class FilterForm():  # Region
    """"""

    def __getattribute__(self, name):
        obj = object.__getattribute__(self, name)

        if isinstance(obj, type) and name != "__class__":  # and issubclass(obj, Region)
            print(name)
            setattr(self, name, obj(self))
            return object.__getattribute__(self, name)
        else:
            return obj


def fun(cls):
    def temp():
        return cls
    return temp


class MetaMessage(type):

    def __new__(mcs, name, bases, attrs, **extra_kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        # return fun(cls)
        return cls

    def __init__(cls, name, bases, dict):
        print("__init__(%r, %r, %r)" % (name, bases, dict))
        print("__init__({0},{1},{2},{3})".format(cls, name, bases, dict))
        type.__init__(cls, name, bases, dict)

    @classmethod
    def __prepare__(mcs, cls, bases, **kwargs):
        print("__prepare__1")
        res = super().__prepare__(mcs, cls, bases, **kwargs)
        return res

    def __call__(cls, *args, **kwargs):
        print("__call__1")
        res = super().__call__(*args, **kwargs)
        print("__call__2")
        return fun(cls)  # res


class Messages(metaclass=MetaMessage):
    m = 1


class Child(Messages):
    ch = 1

    def __init__(self):
        print("Init Child")


ch = Child()
print()
