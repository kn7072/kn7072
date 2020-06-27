plugin_registry = {}


def get_registry():
    class RegMeta(type):
        def __init__(self):
            self.interface_name = None
        def __new__(cls, name, bases, cls_dict):
            new_cls = super(RegMeta, cls).__new__(name, bases, cls_dict)
            return new_cls
    return RegMeta


def get_all_implementations(interface):
    return plugin_registry[interface.__name__]


class IDataGridUI(object):
    __metaclass__ = get_registry()
    provides_ui = None

    def display_my_data(self, data):
        pass
q = IDataGridUI()
