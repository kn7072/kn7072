# -*- coding=utf-8 -*-
import importlib


def dynamic_import(module):
    return importlib.import_module(module)


module = dynamic_import('foo')
module.main()

module_two = dynamic_import('bar')
module_two.main()