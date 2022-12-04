# -*- coding: utf-8 -*-

# https://www.sobyte.net/post/2021-10/python-import/


import sys
from types import ModuleType
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, Loader


class Module(ModuleType):
    def __init__(self, name):
        self.x = 1
        self.name = name


class ExampleLoader(Loader):
    def create_module(self, spec):
        return Module(spec.name)

    def exec_module(self, module):
        module.y = 2


class ExampleFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        return ModuleSpec('module', ExampleLoader())


sys.meta_path = [ExampleFinder()]

if __name__ == "__main__":
    import module

    print(module.x)
    print(module.y)


"""
As you can see from the above example, a loader usually has two important methods create_module and
 exec_module that need to be implemented. If the exec_module method is implemented, then create_module is required.
 If this import mechanism is initiated by an import statement, then the variables corresponding to the module
 object returned by the create_module method will be bound to the current local variables.
 If a module is thus successfully loaded, it will be cached in sys.modules, and if the module is loaded again,
 the sys.modules cache will be referenced directly.

Note that before Python 3.4 finder would return the loader directly instead of the module spec,
 which actually already contains the loader.
"""
