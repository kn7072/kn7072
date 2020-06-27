# -*- coding: utf-8 -*-


class TypedProperty(object):
    def __init__(self, type, default=None):
        self.name = None
        self.type = type
        if default:
            self.default = default
        else:
            self.default = type()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class dd:
    def jjj(self):
        pass
    pass


class y(dd):

    def s(self):
        print('s')

    def x(self, a):
        print(a)

    def t(self, b):
        print(b)


class TypedMeta(type):
    def __new__(cls, name, bases, dict):
        slots = []
        for key, value in dict.items():
            if isinstance(value, TypedProperty):
                value.name = "_" + key
                slots.append(value.name)
        #dict['__slots__'] = slots
        new_class = type.__new__(cls, name, bases, dict)
        return new_class

    def __call__(cls, *args, **kwargs):
        print()


# Базовый класс для объектов, определяемых пользователем
class Typed(y, metaclass=TypedMeta):  # В Python 3 используется синтаксис class Typed(metaclass=TypedMeta) __metaclass__ = TypedMeta
    def __init__(self):
        self.eee = 1

    def met(self):
        print(self.eee)


class Foo(Typed):
    name = TypedProperty(str)
    num = TypedProperty(int, 42)

f = Foo()
x = Typed()
pass
