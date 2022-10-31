# coding: utf-8

"""
9.14. Захват порядка определения атрибутов класса

Задача
Вы хотите автоматически записывать порядок, в котором внутри тела класса
определяются атрибуты и методы, что полезно при различных операциях (напри-
мер, при сериалиации, отображении в базы данных и т. п.).
"""

from collections import OrderedDict


# Набор дескрипторов для различных типов
class Typed:

    _expected_type = type(None)


    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError('Expected ' + str(self._expected_type))
        instance.__dict__[self._name] = value


class Integer(Typed):
    _expected_type = int


class Float(Typed):
    _expected_type = float


class String(Typed):
    _expected_type = str


# Метакласс, который использует OrderedDict для тела класса
class OrderedMeta(type):

    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        order = []
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                order.append(name)
                d['_order'] = order
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return OrderedDict()


class Structure(metaclass=OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self,name)) for name in self._order)


# Пример использования
class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

"""
Краеугольный камень данного рецепта – метод __prepare__(), который определен
в метаклассе OrderedMeta. Этот метод немедленно вызывается при старте опре-
деления класса вместе с именем класса и базовыми классами. Он должен вернуть
объект отображения для использования во время выполнения тела класса. Поря-
док определения легко захватить и сохранить с помощью возвращения OrderedDict
вместо обычного словаря.
"""

s = Stock('GOOG',100,490.1)
s.name
s.as_csv()
t = Stock('AAPL','a lot', 610.23)  # error