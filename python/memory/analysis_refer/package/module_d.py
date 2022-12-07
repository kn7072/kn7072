# -*- coding: utf-8 -*-
from .common import Meta
from .module_c import C


class D(metaclass=Meta):

    def __init__(self, d=2):
        self.instance_c = C(d)
