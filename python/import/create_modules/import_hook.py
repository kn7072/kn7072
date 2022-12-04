# -*- coding: utf-8 -*-

# https://www.sobyte.net/post/2021-10/python-import/

"""
import hook

For simplicity, we did not mention the import mechanism hook in the flowchart above,
 but you can actually add a hook to change sys.meta_path or sys.path to change the
 behavior of the import mechanism. In the example above, we modified sys.meta_path directly, but you can actually
 do that with a hook.

The import hook is used to extend the import mechanism, and it comes in two types.

    The meta hook is called at the very beginning of the import (after looking for cached modules),
     where you can overload the handling of sys.path, frozen module and even built-in modules.
     Just add a new finder to sys.meta_path to register the meta_hook.
    import path hooks are called when path (or package.path) is processed and they take
     care of the entries in sys.path. Just add a new callable to sys.path_hooks to register the import path hook.

"""

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


def example_hook(path):
    # some conditions here
    return ExampleFinder()


sys.path_hooks = [example_hook]
# force to use the hook
sys.path_importer_cache.clear()

if __name__ == "__main__":
    import module

    print(module.x)
    print(module.y)
