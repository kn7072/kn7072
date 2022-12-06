# -*- coding: utf-8 -*-
from .module_c import C
from .common import Meta


class A1(metaclass=Meta):
    pass


class A2(metaclass=Meta):
    a2 = C()
