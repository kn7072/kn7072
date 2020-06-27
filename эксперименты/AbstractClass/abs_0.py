# -*- coding: utf-8 -*-
import abc


class Base(abc.ABC):
    @property
    @abc.abstractmethod
    def value(self):
        return 'Should never reach here'

    @property
    @abc.abstractmethod
    def constant(self):
        return 'Should never reach here'

    def x(self):
        print("x")


obj = Base()
print()