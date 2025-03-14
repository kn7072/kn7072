# -*- coding: utf-8 -*-
# 18.2.8. Абстрактный класс и статические методы
import abc


class Base(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def factory(cls, *args):
        return cls()

    @staticmethod
    @abc.abstractmethod
    def const_behavior():
        return "Should never reach here"


class Implementation(Base):
    def do_something(self):
        pass

    @classmethod
    def factory(cls, *args):
        obj = cls(*args)
        obj.do_something()
        return obj

    @staticmethod
    def const_behavior():
        return "Static behavior differs"


try:
    o = Base.factory()
    print('Base.value:', o.const_behavior())
except Exception as err:
    print('ERROR:', str(err))
    i = Implementation.factory()
    print('Implementation.const_behavior :', i.const_behavior())