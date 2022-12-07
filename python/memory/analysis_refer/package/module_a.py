# -*- coding: utf-8 -*-
from .module_c import C
from .module_d import D
from .common import Meta


class A1(metaclass=Meta):

    def __init__(self, d=2):
        self.d = D(d)


class A2(metaclass=Meta):
    a2 = C()
