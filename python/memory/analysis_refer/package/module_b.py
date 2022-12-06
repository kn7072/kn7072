# -*- coding: utf-8 -*-
from .common import Meta
from package.module_c import C


class B(metaclass=Meta):
    bc = C(2)

