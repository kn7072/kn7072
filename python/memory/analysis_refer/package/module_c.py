# -*- coding: utf-8 -*-
from .common import Meta


class C(metaclass=Meta):
    
    def __init__(self, c=None):
        self.c = c if c else 1
